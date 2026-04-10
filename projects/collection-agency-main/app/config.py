import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

class Config:
    # Flask / security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'

    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///' + os.path.join(PROJECT_ROOT, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # App settings
    DEBTORS_PER_PAGE = int(os.environ.get('DEBTORS_PER_PAGE', 25))

    # Uploads
    # default upload folder (can be overridden via env UPLOAD_FOLDER)
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or os.path.join(PROJECT_ROOT, 'uploads')

    # Max upload size (bytes)
    MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))  # 16 MB default

    # Allowed extensions for general uploads (documents)
    ALLOWED_UPLOAD_EXTENSIONS = set(os.environ.get('ALLOWED_UPLOAD_EXTENSIONS', 'pdf,png,jpg,jpeg,doc,docx,xls,xlsx,txt').split(','))

    # Allowed extensions specifically for Excel import
    ALLOWED_EXTENSIONS_FOR_IMPORT = set(os.environ.get('ALLOWED_EXTENSIONS_FOR_IMPORT', 'xlsx,xls').split(','))

class ProductionConfig(Config):
    FLASK_ENV = 'production'
    DEBUG = False
    TESTING = False

class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    DEBUG = True
    TESTING = False