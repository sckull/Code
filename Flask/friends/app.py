#!/usr/bin/env python3
#SQLAlchemy
#sudo apt-get install python3-sqlalchemy
#apt-get install python3-venv
from flask import Flask, request, render_template_string, render_template, flash, redirect, url_for, session, Response
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from hashlib import md5
from flask_msearch import Search
import random, string
from functools import wraps

app = Flask(__name__,
            static_url_path = '', 
            static_folder   = 'static',
            template_folder = 'templates')

app.config.from_pyfile("config.cfg")
db = SQLAlchemy(app)
search = Search()
search.init_app(app)

#Access
ACCESS = {
    'user':  1,
    'admin': 2
}

#Messing
fake_password = ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(16)).encode('utf-8').hex()

######################
#        MODELS      #
######################
class User(db.Model):
    __tablename__  = 'user'
    __table_args__ = {'sqlite_autoincrement': True}
    __searchable__ = ['name','lastname']
    id       = db.Column(db.Integer,    primary_key = True, autoincrement = True)
    username = db.Column(db.String(80), nullable = False, unique = False )
    name     = db.Column(db.String(80), nullable = False)
    lastname = db.Column(db.String(80), nullable = False)
    email    = db.Column(db.String(120),nullable = False, unique = True)
    password = db.Column(db.String(100),nullable = False)
    info     = db.Column(db.String(320),nullable = False)
    access   = db.Column(db.String(10), nullable = True)
    posts    = db.relationship('Post',  backref  = 'author', lazy = 'dynamic')
    
    def __init__(self, username, name, lastname, email, password, info, access=ACCESS['user']):
        self.username = username
        self.name     = name
        self.lastname = lastname
        self.email    = email
        self.password = password
        self.info     = info
        self.access   = access
    
    def __repr__(self):
        return '<User %r>' % self.username

    def is_admin(self):
        return int(self.access) == ACCESS['admin']
    
    def allowed(self, access_level):
        return int(self.access) >= int(access_level)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

class Post(db.Model):
    __tablename__  = 'post'
    __table_args__ = {'sqlite_autoincrement': True}
    __searchable__ = ['body']
    id        = db.Column(db.Integer, primary_key = True, autoincrement = True)
    body      = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow)
    user_id   = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

######################
#        ERROR       #
######################
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html', fake_password = fake_password), 404

######################
#     DECORATORS     #
######################
#Decorators Login and Access Level
def login_required(log):
    @wraps(log)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return log(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

def requires_access_level(access_level):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not session.get('logged_in'):
                return redirect(url_for('login'))

            if session.get('logged_in') is True:
                user = User.query.get(session['id'])
                if not user.allowed(access_level):
                    flash("You dont have access here!")
                    return redirect(url_for('post'))
                return f(*args, **kwargs)
        return decorated_function
    return decorator

######################
#        GUEST       #
######################
@app.route('/robots.txt')
def robots():
    robots = Response(response = "User-agent: *\nDisallow: /users\nDisallow: /shell.php\nDisallow: /sub7-2.0.exe", status = 200, mimetype = "text/plain")
    robots.headers["Content-Type"] = "text/plain; charset=utf-8"
    return robots

@app.route("/")
@app.route("/index")
def index():
    if  session.get('logged_in') is True:
        return redirect(url_for("home"))
    return render_template('index.html')

@app.route("/register", methods = ["GET", "POST"])
def register():
    if  session.get('logged_in') is True:
        return redirect(url_for("home"))
    if request.method == "POST":
        if not request.form["username"]:
            flash("Username is required", "error")
        elif not request.form["name"]:
            flash("Name is required", "error")
        elif not request.form["lastname"]:
            flash("LastName is required", "error")
        elif not request.form["email"]:
            flash("Email is required", "error")
        elif not request.form["info"]:
            flash("Info is required", "error")
        else:
            hashed_password = generate_password_hash(request.form["password"], method = 'sha256')
            user = User(request.form["username"], request.form["name"], request.form["lastname"], request.form["email"], hashed_password, request.form["info"])
            reg = User.query.filter_by(username = request.form["email"]).first()

            if bool(reg):
                flash("Email already in use, take another username and email.")
                return redirect(url_for("register"))
            if not reg:
                db.session.add(user)
                db.session.commit()
                flash("User was successfully registered!.")
                return redirect(url_for("login"))

    return render_template("register.html")

@app.route("/login", methods = ["GET", "POST"])
def login():
    #print(session)
    session['leader'] = True
    print(session)
    if  session.get('logged_in') is True:
        return redirect(url_for("home"))

    if request.method == "POST":
        if not request.form["email"]:
            flash("Email is required", "error")
        elif not request.form["password"]:
            flash("Password is required", "error")
        else:
            user = User.query.filter_by(email = request.form["email"]).first()
            if user:
                if check_password_hash(user.password, request.form["password"]):
                    flash('You have successfully logged in.', "success")
                    session['logged_in'] = True
                    session['id']        = user.id
                    session['email']     = user.email
                    session['username']  = user.username
                    session['access']    = user.access
                    session['is_admin']  = user.is_admin()
                    return redirect(url_for("home"))
                else:                    
                    flash('Email or Password Incorrect', "error")
                    return redirect(url_for('login'))
            else:
                flash('User doesn\'t exists.', "error")
                return redirect(url_for("register"))    
    return render_template("login.html")

@app.route('/logout')
@login_required
def logout():
    session.clear()
    return redirect(url_for('login'))

######################
#         USER       #
######################
@app.route("/home", methods = ['GET'])
@login_required
def home():
    user  = User.query.get(session['id'])
    if user:
        users = User.query.filter_by(access='1').all() #get all users
        return render_template('home.html', user = user, users = users)
    else:
        return render_template('404.html',fake_password = fake_password), 404

@app.route("/post", methods = ["GET","POST"])
@login_required
def post():
    if request.method == "POST":
        if not request.form["body"]:
            flash("Write something interesting.", "error")
        else:         
            post = Post(body = request.form["body"], author = User.query.get(session['id']))
            db.session.add(post)
            db.session.commit()
            flash("New Post!.")
            return redirect(url_for("post"))    
    user_post = User.query.get(session['id'])
    posts = user_post.posts.order_by(Post.timestamp.desc()).all()
    return render_template("post.html", posts = posts, user = user_post)

'''@app.route("/search", methods = ["GET","POST"])
@login_required
def search():    
    return render_template_string(request.args['a'])'''

@app.route('/user/<int:id>/', methods = ['GET', 'POST'])
@login_required
def user(id):
    #Logged User
    user = User.query.get(session['id'])
    #Actual user visited
    user_visit = User.query.get(id)
    if user_visit:
        posts = user_visit.posts.all()
        return render_template("post.html", posts = posts, user_visit = user_visit, user = user)
    else:
        return render_template('404.html',fake_password = fake_password), 404

######################
#        ADMIN       #
######################
@app.route("/users", methods = ["GET", "POST"])
@login_required
@requires_access_level(ACCESS['admin'])
def users():    
    user = User.query.get(session['id'])        
    if not user.is_admin():
        return redirect(url_for('post'))
    users = User.query.order_by(User.id.asc()).all()
    user  = User.query.get(session['id'])
    return render_template("users.html", users = users, user = user)

@app.route("/admins", methods=["GET"])
@login_required
@requires_access_level(ACCESS['admin'])
def admins():
    user  = User.query.get(session['id'])
    if user:
        admins = User.query.filter_by(access='2').all() #get all admins
        return render_template("admins.html", user = user, users = admins)

@app.route('/insert', methods = ['POST'])
@login_required
@requires_access_level(ACCESS['admin'])
def insert():
    if request.method == 'GET':
            return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form['username']
        name = request.form['name']
        lastname = request.form['lastname']
        email = request.form['email']
        password = generate_password_hash(request.form["password"], method = 'sha256')
        info = request.form['info']
        access = request.form['access']

        data = User(username, name, lastname, email, password, info, access)
        db.session.add(data)
        db.session.commit() 
        flash("User Inserted Successfully") 
        return redirect(url_for('users'))

@app.route('/update', methods = ['GET', 'POST'])
@login_required
@requires_access_level(ACCESS['admin'])
def update():
    if request.method == 'GET':
            return redirect(url_for('index'))
    if request.method == 'POST':
        user = User.query.get(request.form.get('id'))
        if user:
            user.username = request.form['username']
            user.name = request.form['name']
            user.lastname = request.form['lastname']
            user.email = request.form['email']
            user.password = generate_password_hash(request.form["password"], method = 'sha256')
            user.info = request.form['info']
            user.access = request.form['access']
            db.session.commit()
            flash("User Updated Successfully") 
            return redirect(url_for('users'))
        else:
            flash("User not found.")
            return redirect(url_for('users'))

@app.route('/delete/<int:id>/', methods = ['GET', 'POST'])
@login_required
@requires_access_level(ACCESS['admin'])
def delete(id):    
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        flash("User Deleted Successfully") 
        return redirect(url_for('users'))
    else:
        flash("User not found.")
        return redirect(url_for('users'))

######################
#   SEARCH CONTENT   #
######################
@app.route('/search', methods = ['GET', 'POST'])
@login_required
@requires_access_level(ACCESS['admin'])
def search():
    user  = User.query.get(session['id'])
    if request.method == 'POST':
        keyword = request.form.get('keyword')
        if keyword:
            posts = Post.query.msearch(keyword,fields=['body'],limit=10).all()
            users = User.query.msearch(keyword,fields=['name', 'lastname'],limit=10).all()
            #q = db.session.query(User).filter(User.username.ilike(keyword)).first()
            #print(q)
            return render_template('search.html', user = user, users = users, posts = posts, keyword = keyword)
    return render_template('search.html', user = user)

if __name__ == "__main__":
    db.create_all()
    app.run(host='0.0.0.0', port=8080)

"""
UTILS

hashed_password = generate_password_hash('123', method = 'sha256')
user = User('r', 'r', 'r', 'r@r.com', hashed_password,'nothing',access=ACCESS['admin'])        
db.session.add(user)
db.session.commit()
"""
