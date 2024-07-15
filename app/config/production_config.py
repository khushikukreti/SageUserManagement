from .base_config import Config

class ProductionConfig(Config):
    SECRET_KEY = "your_production_secret_key"
    DATABASE_URL = "postgresql://username:password@production_host/production_db"
