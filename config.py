import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    DOWNLOAD_FOLDER = os.environ.get('DOWNLOAD_FOLDER') or 'downloads'
    DEBUG = os.environ.get('FLASK_DEBUG') or False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB limit for file uploads
