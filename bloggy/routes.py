# App
from app import db, app

# flask
from flask_login import login_required, logout_user, current_user, login_user
from flask import Flask, render_template, session, flash, redirect, url_for, request

# Models
from models import User, Tag, Post, Role

# Forms
from forms import LoginForm, RegisterForm, EditForm, CreatePost, EditPost, tag_loader, CreateTag, EditTag, NewUserForm, EditUserForm, ChangePassword

# Utils
from datetime import datetime
import re, os, hashlib, pathlib
from werkzeug.utils import secure_filename
from uuid import uuid1

# Markdown
import markdown
import markdown.extensions.fenced_code
from markdown.extensions.toc import TocExtension
from pygments.formatters import HtmlFormatter

# Permissions
from flask_principal import Principal, RoleNeed, UserNeed, Permission, Identity, identity_changed, identity_loaded, AnonymousIdentity
from flask import current_app

# Flask-Principal
# Permission
admin = Permission(RoleNeed('admin'))
editor_or_admin = Permission(RoleNeed('editor'), RoleNeed('admin'))

@identity_loaded.connect_via(app)
def on_identity_loaded(sender, identity):
    identity.user = current_user

    if hasattr(current_user, 'id'):
        identity.provides.add(UserNeed(current_user.id))

    if hasattr(current_user, 'roles'):
        for role in current_user.roles:
            identity.provides.add(RoleNeed(role.name))

# Code 403
@app.errorhandler(403)
def handle_error(e):
    return render_template('errors/403.html'), 403

# Check Permissions for Templates
# source: https://flask.palletsprojects.com/en/2.1.x/appcontext/
@app.context_processor
def utility_processor():
    def has_role_admin(roles):
        return True if 'admin' in [x.name for x in roles] else False
    return dict(has_role_admin = has_role_admin)


# -----------------------------------------------------------------------------------------------------------------
# POSTS
# -----------------------------------------------------------------------------------------------------------------
@app.route('/admin/posts', methods = ['GET'])
@login_required
@editor_or_admin.require(http_exception=403)
def posts():
    posts = Post.query.order_by(Post.timestamp).all()
    return render_template('posts/posts.html', posts = posts)

@app.route('/admin/post/new', methods = ['GET', 'POST'])
@login_required
@editor_or_admin.require(http_exception=403)
def new_post():
    form = CreatePost()
    
    if form.validate_on_submit():
        tags = form.tags.data
        featured_image = ''
        
        # Image Featured
        if form.image.data:
            f = form.image.data
            filename = secure_filename(f.filename)
            image_filename = str(uuid1())[:10] + hashlib.md5(filename.encode('utf-8')).hexdigest()[:10] + pathlib.Path(filename).suffix
            f.save(os.path.join(
                app.config['UPLOAD_IMAGE_BLOG_FOLDER'], image_filename
                )
            )
            featured_image = app.config['UPLOAD_IMAGE_BLOG_FOLDER'] + image_filename

        if featured_image:
            post = Post(title = form.title.data, 
                    body = form.body.data, 
                    timestamp = form.timestamp.data, 
                    published = form.published.data,
                    user_id = current_user.id,
                    last_edit = datetime.utcnow(),
                    description = form.description.data,
                    featured_image = featured_image)
        else:
            post = Post(title = form.title.data, 
                    body = form.body.data, 
                    timestamp = form.timestamp.data, 
                    published = form.published.data,
                    user_id = current_user.id,
                    last_edit = datetime.utcnow(),
                    description = form.description.data,)       

        for tag in tags:
            tag_exist = Tag.query.filter_by(name=tag.name).first()

            if not tag_exist:
                _tag = Tag(name = tag)
                _tag.posts.append(post)
                db.session.add(_tag)
            else:
                tag_exist.posts.append(post)
        
        db.session.add(post)
        db.session.commit()
        flash("Post has been saved!","success")
        return redirect(url_for('posts'))
    return render_template('posts/new_post.html', form = form)

@app.route('/admin/post/edit/<id>', methods = ['GET', 'POST'])
@login_required
@editor_or_admin.require(http_exception=403)
def edit_post(id):
    post = Post.query.filter_by(id = id).first()    
    
    form = EditPost(title = post.title,
                    timestamp = post.timestamp,
                    published = post.published,
                    description = post.description,
                    tags = post.tags,
                    featured_image = post.featured_image)

    if form.validate_on_submit():        
        """ just worked btw """
        post_tags = [ i.name for i in post.tags]

        # Remove tags
        new = set((x.name) for x in form.tags.data)
        difference = [ x for x in post.tags if (x.name) not in new ]
        #print(difference)        

        for tag in difference:
            _tag = Tag.query.filter_by(name = tag.name).first()
            _tag.posts.remove(post)

        # Add tags
        for tag in form.tags.data:
            if tag.name not in post_tags:
                _tag = Tag.query.filter_by(name = tag.name).first()
                _tag.posts.append(post)
                #print("Added: " + str(tag) + " *****")
        """ just worked btw """
        
        featured_image = ''
        if form.image.data:
            f = form.image.data
            filename = secure_filename(f.filename)
            image_filename = str(uuid1())[:10] + hashlib.md5(filename.encode('utf-8')).hexdigest()[:10] + pathlib.Path(filename).suffix
            f.save(os.path.join(
                app.config['UPLOAD_IMAGE_BLOG_FOLDER'], image_filename
                )
            )
            featured_image = app.config['UPLOAD_IMAGE_BLOG_FOLDER'] + image_filename

        if featured_image:
            post.title = form.title.data
            post.body = form.body.data
            post.timestamp = form.timestamp.data        
            post.published = form.published.data
            post.description = form.description.data
            post.featured_image = featured_image            
            post.last_edit = datetime.utcnow()
        else:
            post.title = form.title.data
            post.body = form.body.data
            post.timestamp = form.timestamp.data        
            post.published = form.published.data
            post.description = form.description.data
            post.last_edit = datetime.utcnow()

        db.session.commit()
        flash("Post has been saved!","success")
        return redirect(url_for('posts'))
        
    return render_template('posts/edit_post.html', form = form, post = post)

@app.route('/admin/post/delete/<id>', methods=['GET'])
@login_required
@editor_or_admin.require(http_exception=403)
def delete_post(id):
    if id:
        post = Post.query.filter_by(id=id).first()
        db.session.delete(post)
        db.session.commit()
        flash("Post has been deleted!","success")
        return redirect(url_for('posts'))
    else:
        return redirect(url_for('posts'))

@app.route('/admin/post/preview/<id>')
@login_required
@editor_or_admin.require(http_exception=403)
def post_preview(id):
    # style == name_style (pygments) , cssclass == name_class_to_use_extensions
    formatter = HtmlFormatter(style = "pastie", 
                              full = True, 
                              cssclass = "codehilite").get_style_defs()

    md = markdown.Markdown(
        extensions = ["fenced_code", "codehilite", 
                        TocExtension( baselevel = 3, 
                                      title = "Table of Contents", 
                                      anchorlink = True, 
                                      permalink = " &#128279;")
                        ]
                    )

    post = Post.query.filter_by( id = id).first()
    post.body = md.convert(post.body)

    return render_template("posts/post_preview.html", post = post, css_style = "<style>" + formatter + "</style>")

# -----------------------------------------------------------------------------------------------------------------
# TAGS
# -----------------------------------------------------------------------------------------------------------------
@app.route('/admin/tags')
@login_required
@editor_or_admin.require(http_exception=403)
def tags():
    tags = Tag.query.order_by(Tag.name).all()
    return render_template('tags/tags.html', tags = tags)

@app.route('/admin/tag/new', methods = ['GET', 'POST'])
@login_required
@editor_or_admin.require(http_exception=403)
def new_tag():
    form_tag = CreateTag()

    if form_tag.validate_on_submit():        
        tag = Tag(name = form_tag.name.data,
                  description = form_tag.description.data
                  )        
        db.session.add(tag)
        db.session.commit()
        flash("Tag has been created!","success")
        return redirect(url_for('tags'))

    return render_template('tags/new_tag.html', form = form_tag)

@app.route('/admin/tag/edit/<id>', methods=['GET', 'POST'])
@login_required
@editor_or_admin.require(http_exception=403)
def edit_tag(id):
    tag = Tag.query.filter_by(id=id).first()

    form = EditTag(name = tag.name,
                   description = tag.description)

    if form.validate_on_submit():
        """ validate if name tag exists """
        if tag.name != form.name.data:
            name_exists = Tag.query.filter_by(name=form.name.data).first()
            if name_exists:
                flash("Tag name already exists. Please choose a different one.","warning")
                return redirect(url_for('edit_tag', id = tag.id))
        """ validate if name tag exists """

        tag.name = form.name.data
        tag.description = form.description.data
        db.session.commit()
        flash("Post has been saved!","success")
        return redirect(url_for('tags'))
    return render_template('tags/edit_tag.html', form = form, tag = tag)

@app.route('/admin/tag/delete/<id>', methods=['GET'])
@login_required
@editor_or_admin.require(http_exception=403)
def delete_tag(id):
    if id:
        tag = Tag.query.filter_by(id=id).first()
        db.session.delete(tag)
        db.session.commit()
        flash("Post has been deleted!","success")
        return redirect(url_for('tags'))
    else:
        return redirect(url_for('tags'))


# -----------------------------------------------------------------------------------------------------------------
# Login, Register, Profile
# -----------------------------------------------------------------------------------------------------------------
@app.route('/admin/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(first_name = form.first_name.data, 
                    last_name  = form.last_name.data, 
                    email      = form.email.data, 
                    username   = form.username.data)        
        user.set_password(form.password.data)        
        db.session.add(user)
        # Default role is Editor
        role = Role.query.filter_by(name='editor').first()
        user.roles.append(role)
        db.session.commit()        
        
        flash("You have registered!","success")
        return redirect(url_for('login'))

    return render_template("register.html", form=form)

@app.route('/admin/', methods=['GET', 'POST'])
@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form = LoginForm(request.form)

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.check_password(password=form.password.data):
            login_user(user)

            identity_changed.send(current_app._get_current_object(), identity = Identity(user.id))

            flash(f'Welcome {user.get_username()}','info')
            return redirect(url_for('posts'))
        flash('Invalid username/password combination','warning')

        return redirect(url_for('login'))
    return render_template('login.html', form=form)    

@app.route('/admin/logout')
@login_required
@editor_or_admin.require(http_exception=403)
def logout():
    logout_user()
    identity_changed.send(current_app._get_current_object(), identity=AnonymousIdentity())
    return redirect(url_for('login'))

@app.route('/admin/profile', methods=['GET', 'POST'])
@login_required
@editor_or_admin.require(http_exception=403)
def profile():
    actual_user = User.query.filter_by(id=current_user.id).first()

    form = EditForm(first_name = actual_user.first_name,
                    last_name  = actual_user.last_name,
                    username   = actual_user.username,
                    email      = actual_user.email,
                    job        = actual_user.job,
                    about      = actual_user.about,
                    twitter    = actual_user.twitter,
                    facebook   = actual_user.facebook,
                    instagram  = actual_user.instagram,
                    linkedin   = actual_user.linkedin,
                    github     = actual_user.github,
                    image      = actual_user.image)

    password_form = ChangePassword()

    if form.validate_on_submit():
        user = User.query.filter_by(id = current_user.id).first()
        user.first_name = form.first_name.data
        user.last_name  = form.last_name.data
        user.username   = form.username.data
        user.email      = form.email.data
        user.job        = form.job.data
        user.about      = form.about.data

        user.twitter    = form.twitter.data
        user.facebook   = form.facebook.data
        user.instagram  = form.instagram.data
        user.linkedin   = form.linkedin.data
        user.github     = form.github.data

        if request.files['image']:
            image_name = secure_filename(request.files['image'].filename)
            image_filename = str(uuid1())[:10] + hashlib.md5(image_name.encode('utf-8')).hexdigest()[:10] + pathlib.Path(image_name).suffix
            saver = request.files['image']
            saver.save(
                os.path.join(
                    app.config['UPLOAD_IMAGE_FOLDER'], image_filename
                    )
                )
            print(image_filename)            
            user.image = app.config['UPLOAD_IMAGE_FOLDER'] + image_filename
        
        db.session.commit()        
        flash("Changes done!","success")
        return redirect(url_for('profile'))
    
    
    return render_template("profile.html", actual_user = actual_user, form = form, password_form = password_form)

@app.route('/admin/change_password', methods=['POST'])
@login_required
@editor_or_admin.require(http_exception=403)
def change_password():
    actual_user = User.query.filter_by(id=current_user.id).first()
    password_form = ChangePassword()

    if password_form.validate_on_submit():
        actual_user.set_password(password_form.password.data)
        db.session.commit()
        flash("Password Changed!","success")
        return redirect(url_for('profile'))

@app.route('/admin/profile/<int:id>', methods=['GET'])
@login_required
@editor_or_admin.require(http_exception=403)
def profile_view(id):
    user = User.query.filter_by(id = id).first()
    posts = Post.query.filter(Post.user_id == id).all()
    return render_template('profile_view.html', user = user, posts = posts)

# -----------------------------------------------------------------------------------------------------------------
# User Manager
# -----------------------------------------------------------------------------------------------------------------
@app.route('/admin/users', methods=['GET'])
@login_required
@admin.require(http_exception=403)
def users():
    users = User.query.order_by(User.username).all()
    return render_template('users/users.html', users = users)

@app.route('/admin/new_user', methods=['GET','POST'])
@login_required
@admin.require(http_exception=403)
def new_user():

    form = NewUserForm(request.form)

    if form.validate_on_submit():
        
        user = User(first_name = form.first_name.data,
                    last_name  = form.last_name.data,
                    username   = form.username.data,
                    email      = form.email.data,
                    job        = form.job.data,
                    about      = form.about.data,
                    twitter    = form.twitter.data,
                    facebook   = form.facebook.data,
                    instagram  = form.instagram.data,
                    linkedin   = form.linkedin.data,
                    github     = form.github.data)

        user.set_password(form.password.data)

        if request.files['image']:
            image_name = secure_filename(request.files['image'].filename)
            image_filename = str(uuid1())[:10] + hashlib.md5(image_name.encode('utf-8')).hexdigest()[:10] + pathlib.Path(image_name).suffix
            saver = request.files['image']
            saver.save(
                os.path.join(
                    app.config['UPLOAD_IMAGE_FOLDER'], image_filename
                    )
                )
            user.image = app.config['UPLOAD_IMAGE_FOLDER'] + image_filename 

        if form.roles.data:
            for role in form.roles.data:
                user.roles.append(role)

        # user.roles.append(Role(name='editor'))
        db.session.add(user)
        db.session.commit()

        flash("User Created!","success")
        return redirect(url_for('users'))

    return render_template('users/new_user.html', form = form)

@app.route('/admin/edit_user/<id>', methods=['GET','POST'])
@login_required
@admin.require(http_exception=403)
def edit_user(id):
    user = User.query.filter_by(id = id).first()
    
    form = EditUserForm(first_name = user.first_name,
                        last_name  = user.last_name,
                        username   = user.username,
                        email      = user.email,
                        job        = user.job,
                        about      = user.about,
                        twitter    = user.twitter,
                        facebook   = user.facebook,
                        instagram  = user.instagram,
                        linkedin   = user.linkedin,
                        github     = user.github,
                        image      = user.image,
                        roles      = user.roles)

    if form.validate_on_submit():        
        user.first_name = form.first_name.data
        user.last_name  = form.last_name.data        
        user.job        = form.job.data
        user.about      = form.about.data
        user.twitter    = form.twitter.data
        user.facebook   = form.facebook.data
        user.instagram  = form.instagram.data
        user.linkedin   = form.linkedin.data
        user.github     = form.github.data

        if request.files['image']:
            image_name = secure_filename(request.files['image'].filename)
            image_filename = str(uuid1())[:10] + hashlib.md5(image_name.encode('utf-8')).hexdigest()[:10] + pathlib.Path(image_name).suffix
            saver = request.files['image']
            saver.save(
                os.path.join(
                    app.config['UPLOAD_IMAGE_FOLDER'], image_filename
                    )
                )
            user.image = app.config['UPLOAD_IMAGE_FOLDER'] + image_filename

        if form.username.data:
            if user.username != form.username.data:
                existing_username = User.query.filter_by(username=form.username.data).first()
                if existing_username:                    
                    flash("That username already exists. Please choose a different one.","warning")
                    return redirect(url_for('edit_user', id = id))
                else:
                    user.username = form.username.data

        if form.email.data:
            if user.email != form.email.data:
                existing_email = User.query.filter_by(email=form.email.data).first()                
                if existing_email:
                    flash("That email already exists. Please choose a different one.","warning")
                    return redirect(url_for('edit_user', id = id))
                else:
                    user.email = form.email.data

        # remove and add roles
        """ just worked btw """
        # Remove roles
        new = set((x.name) for x in form.roles.data)
        difference = [ x for x in user.roles if (x.name) not in new ]
        #print(difference)

        for role in difference:
            _role = Role.query.filter_by(name = role.name).first()
            _role.user_roles.remove(user)

        # add roles
        user_roles = [ i.name for i in user.roles]
        for role in form.roles.data:
            if role.name not in user_roles:
                _role = Role.query.filter_by(name=role.name).first()
                _role.user_roles.append(user)
        """ just worked btw """

        db.session.commit()            
        flash("Changes done!","success")
        return redirect(url_for('users'))

    return render_template("users/edit_user.html", form = form, user = user)

@app.route('/admin/change_password_user/<id>', methods=['GET','POST'])
@login_required
@admin.require(http_exception=403)
def change_password_user(id):
    user = User.query.filter_by(id=id).first()
    form = ChangePassword()

    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash("Changes done!","success")
        return redirect(url_for('users'))

    return render_template('users/change_password.html', form = form, user = user)

@app.route('/admin/del_user/<id>', methods=['GET'])
@login_required
@admin.require(http_exception=403)
def del_user(id):
    if id:
        user = User.query.filter_by(id=id).first()
        db.session.delete(user)
        db.session.commit()
        flash("User has been deleted!","success")
        return redirect(url_for('users'))
    else:
        return redirect(url_for('users'))

# -----------------------------------------------------------------------------------------------------------------
# Public Blog
# -----------------------------------------------------------------------------------------------------------------
@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():    
    posts = Post.query.filter_by(published = True).all()
    tags = Tag.query.order_by(Tag.name).all()
    return render_template("blog_index.html", posts = posts, tags = tags)

@app.route('/post/<id>', methods=['GET'])
def post(id):    
    formatter = HtmlFormatter(style = "pastie", 
                              full = True, 
                              cssclass = "codehilite").get_style_defs()
    md = markdown.Markdown(
        extensions = ["fenced_code", "codehilite", 
                        TocExtension( baselevel = 3, 
                                      title = "Table of Contents", 
                                      anchorlink = True, 
                                      permalink = " &#128279;")
                        ]
                    )
    post = Post.query.filter_by( id = id).first()
    post.body = md.convert(post.body)
    return render_template("blog/post.html", post = post, css_style = "<style>" + formatter + "</style>")

@app.route('/tag/<id>', methods=['GET'])
def tag(id):
    tag = Tag.query.filter_by(id = id).first()    
    return render_template("blog/tag.html",tag=tag)

@app.route('/tags', methods=['GET'])
def tags_blog():
    tags = Tag.query.all()
    return render_template("blog/tags.html", tags = tags)

@app.route('/search', methods=['GET'])
def search():
    search = request.args.get('q')
    if search:        
        posts = Post.query.filter(Post.title.like("%"+search+"%")).all()
        print(posts)
    else:
        flash("a","warning")
        return redirect(url_for('index'))
    return render_template("blog/search.html",posts = posts)

@app.route('/user/<id>', methods=['GET'])
def editor(id):
    user = User.query.filter_by(id = id).first()
    posts = Post.query.filter(Post.user_id == id).all()
    return render_template("blog/user.html", user = user, posts = posts)