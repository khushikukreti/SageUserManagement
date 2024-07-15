from .base_config import Config

class DevelopmentConfig(Config):
    SECRET_KEY = "your_development_secret_key"
    DATABASE_URL = "postgresql://postgres:postgres@localhost/USER_PET"
