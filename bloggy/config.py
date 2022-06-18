SECRET_KEY = b'_5#y2L"F4Q8z\n\xec]/'
SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
SQLALCHEMY_TRACK_MODIFICATIONS = True
UPLOAD_IMAGE_FOLDER = 'static/images/'
UPLOAD_IMAGE_BLOG_FOLDER = 'static/images/blog/'
FILE_EXTENSIONS_ALLOWED = ['.jpg','.jpeg','.png','.gif']

# recaptcha
RECAPTCHA_DATA_ATTRS = {'theme': 'light'}
# site key
RECAPTCHA_PUBLIC_KEY = "6Leg9FAgAAAAAOsI0hFri84KxTKgJr5Q1XuboyQg"
# private key
RECAPTCHA_PRIVATE_KEY = "6Leg9FAgAAAAAAZMJnOP-UbV4qBmSJOp3QEmrT6D"
