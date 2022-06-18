# App
from app import db

# Fields
from flask_wtf import FlaskForm, RecaptchaField
from wtforms import StringField, PasswordField, validators, SubmitField, ValidationError, BooleanField, DateField, TextAreaField, SelectMultipleField, FileField, RadioField, widgets

from wtforms.fields.html5 import EmailField
from flask_wtf.file import FileAllowed

# Select2
from flask_select2.model.fields import AjaxSelectField, AjaxSelectMultipleField
from flask_select2.contrib.sqla.ajax import QueryAjaxModelLoader
from flask_admin.form.widgets import Select2Widget
from wtforms.ext.sqlalchemy.fields import QuerySelectField, QuerySelectMultipleField

# Models
from models import User, Post, Tag, Role

# Utils
from flask_login import current_user
from datetime import datetime

"""
MultiCheckBox
source : https://stackoverflow.com/questions/70563907/display-wtforms-selectmultiplefield-display-as-drop-down-and-not-list
"""
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()

class LoginForm(FlaskForm):
    username = StringField(
        'Username', [
            validators.DataRequired("Please enter your user id")
        ]
    )
    password = PasswordField(
        'Password', [
            validators.DataRequired("Please enter your user id")
        ]
    )
    submit = SubmitField()


class RegisterForm(FlaskForm):
    first_name = StringField(
        'First Name', [
            validators.DataRequired("Please enter your name.")
        ]
    )
    last_name = StringField(
        'Last Name', [
            validators.DataRequired("Please enter your last name.")
        ]
    )
    email = EmailField(
        'Email', [
            validators.DataRequired('Please enter your email')
        ]
    )

    username = StringField(
        'Username', [
            validators.DataRequired("Please enter an username.")
        ]
    )
    password = PasswordField(
        'Password', [
            validators.DataRequired('Please enter your password'),
            validators.EqualTo(
                    'confirm_password', 
                    message = 'Passwords must match'
                )
        ]
    )
    confirm_password = PasswordField('Repeat Password')
    recaptcha = RecaptchaField()
    submit = SubmitField()

    def validate_username(self, username):
        existing_username = User.query.filter_by(username = username.data).first()
        if existing_username:
            raise ValidationError('That username already exists. Please choose a different one.')

    def validate_email(self, email):
        existing_email = User.query.filter_by(email = email.data).first()
        if existing_email:
            raise ValidationError('That email already exists. Please choose a different one.')

class EditForm(FlaskForm):
    first_name = StringField(
        'First Name', [
            validators.DataRequired("Please enter your name.")
        ]
    )
    last_name  = StringField(
        'Last Name', [
            validators.DataRequired("Please enter your last name.")
        ]
    )
    email      = EmailField(
        'Email', [
            validators.DataRequired('Please enter your email')
        ]
    )
    username   = StringField(
        'Username', [
            validators.DataRequired("Please enter an username.")
        ]
    )
    job        = StringField('Job')
    about      = TextAreaField('About')
    image      = FileField(
        'Profile Image', 
        validators = [
            FileAllowed(['jpg', 'jpeg','png'], 'Images only!')
        ]
    )
    twitter    = StringField('Twitter')
    facebook   = StringField('Facebook')
    instagram  = StringField('Instagram')
    linkedin   = StringField('Linkedin')
    github     = StringField('GitHub')
    """
    password = PasswordField('Password', [
        validators.EqualTo(
            'confirm_password', 
            message = 'Passwords must match.'
        )
    ])
    confirm_password = PasswordField('Repeat Password')
    """
    submit = SubmitField()

    def validate_username(self, username):
        if current_user.username != username.data:            
            existing_username = User.query.filter_by(username = username.data).first()
            if existing_username:
                raise ValidationError('That username already exists. Please choose a different one.')

    def validate_email(self, email):
        if current_user.email != email.data:
            existing_email = User.query.filter_by(email = email.data).first()
            if existing_email:
                raise ValidationError('That email already exists. Please choose a different one.')
    """
    def validate_image(self, image):
        # field.data is not working 
        ext = pathlib.Path(secure_filename(request.files['image'].filename)).suffix
        if ext not in app.config['FILE_EXTENSIONS_ALLOWED']:
            raise ValidationError('Invalid File.')
    """ 

def roles_choices():
    return Role.query

class NewUserForm(FlaskForm):
    first_name = StringField(
        'First Name', [
            validators.DataRequired("Please enter your name.")
        ]
    )
    last_name = StringField(
        'Last Name', [
            validators.DataRequired("Please enter your last name.")
        ]
    )
    email = EmailField(
        'Email', [
            validators.DataRequired('Please enter your email')
        ]
    )
    username = StringField(
        'Username', [
            validators.DataRequired("Please enter an username.")
        ]
    )
    job        = StringField('Job')
    about      = TextAreaField('About')
    image      = FileField(
        'Profile Image', 
        validators = [
            FileAllowed(['jpg', 'jpeg','png'], 'Images only!')
        ]
    )
    twitter    = StringField('Twitter')
    facebook   = StringField('Facebook')
    instagram  = StringField('Instagram')
    linkedin   = StringField('Linkedin')
    github     = StringField('GitHub')
    roles      = QuerySelectMultipleField(
            'Roles', 
            query_factory = roles_choices, 
            allow_blank = True, 
            get_label = 'name',
            blank_text = u'123423'
        )

    password = PasswordField('Password', [
        validators.DataRequired('Please enter your password'),
        validators.EqualTo(
            'confirm_password', 
            message = 'Passwords must match')
        ]
    )
    confirm_password = PasswordField('Repeat Password')
    submit = SubmitField()

    def validate_username(self, username):
        existing_username = User.query.filter_by(username = username.data).first()
        if existing_username:
            raise ValidationError('That username already exists. Please choose a different one.')

    def validate_email(self, email):
        existing_email = User.query.filter_by(email = email.data).first()
        if existing_email:
            raise ValidationError('That email already exists. Please choose a different one.')

class EditUserForm(FlaskForm):
    first_name = StringField(
        'First Name', [
            validators.DataRequired("Please enter your name.")
        ]
    )
    last_name = StringField(
        'Last Name', [
            validators.DataRequired("Please enter your last name.")
        ]
    )
    email = EmailField(
        'Email', [
            validators.DataRequired('Please enter your email')
        ]
    )
    username = StringField(
        'Username', [
            validators.DataRequired("Please enter an username.")
        ]
    )
    job        = StringField('Job')
    about      = TextAreaField('About')
    image      = FileField(
        'Profile Image', 
        validators = [
            FileAllowed(['jpg', 'jpeg','png'], 'Images only!')
        ]
    )
    twitter    = StringField('Twitter')
    facebook   = StringField('Facebook')
    instagram  = StringField('Instagram')
    linkedin   = StringField('Linkedin')
    github     = StringField('GitHub')
    roles      = QuerySelectMultipleField(
            'Roles', 
            query_factory = roles_choices, 
            get_label = 'name'
        )
    submit = SubmitField()
    # validation for email and username in route

class ChangePassword(FlaskForm):
    password = PasswordField(
        'Password', [
            validators.DataRequired('Please enter your password'),
            validators.EqualTo(
                'confirm_password', 
                message = 'Passwords must match'
            )
        ]
    )
    confirm_password = PasswordField('Repeat Password')
    submit = SubmitField()

"""
Tag Loader Ajax
"""
tag_loader = QueryAjaxModelLoader(
    name        = 'tag',
    session     = db.session,
    model       = Tag,
    fields      = ['name'],
    order_by    = [Tag.name.asc()],
    page_size   = 20,
    placeholder = "Select a Tag"
)

class CreatePost(FlaskForm):
    title       = StringField(
        'Title', [
            validators.DataRequired("Please enter a title.")
        ]
    )
    body        = TextAreaField(
        'Body', [
            validators.DataRequired("Please write some content.")
        ]
    )
    description = TextAreaField(
        'Description', [
            validators.DataRequired("Please write some content.")
        ]
    )
    timestamp   = DateField(
        'Date', 
        format = '%Y-%m-%d', 
        default = datetime.now()
    )
    published   = BooleanField('Public?')
    image       = FileField(
        'Featured Image', 
        validators = [
            FileAllowed(['jpg', 'jpeg','png'], 'Images only!')
        ]
    )
    tags        = AjaxSelectMultipleField(
        loader      = tag_loader,
        label       = 'Tags',
        allow_blank = False
    )
    submit      = SubmitField()

class EditPost(FlaskForm):
    title       = StringField(
        'Title', [
            validators.DataRequired("Please enter a title.")
        ]
    )
    body        = TextAreaField(
        'Body', [
            validators.DataRequired("Please write some content.")
        ]
    )
    description = TextAreaField(
        'Description', [
            validators.DataRequired("Please write some content.")
        ]
    )
    timestamp   = DateField(
        'Date', 
        format = '%Y-%m-%d', 
        default = datetime.now()
    )
    published   = BooleanField('Public')
    image       = FileField(
        'Featured Image', 
        validators = [
            FileAllowed(['jpg', 'jpeg','png'], 'Images only!')
        ]
    )
    tags        = AjaxSelectMultipleField(
        loader      = tag_loader,
        label       = 'Tags',
        allow_blank = False
    )
    submit      = SubmitField()

class CreateTag(FlaskForm):
    name        = StringField(
        'Name', [
            validators.DataRequired("Please enter a name.")
        ]
    )
    description = StringField(
        'Description', [
            validators.DataRequired("Please enter a description.")
        ]
    )
    submit      = SubmitField()

    def validate_name(self, name):
        name_exists = Tag.query.filter_by(name = name.data).first()
        if name_exists:
            raise ValidationError('Tag name already exists. Please choose a different one.')

class EditTag(FlaskForm):
    name        = StringField(
        'Name', [
            validators.DataRequired("Please enter a name.")
        ]
    )
    description = StringField(
        'Description', [
            validators.DataRequired("Please enter a description.")
        ]
    )
    submit      = SubmitField()