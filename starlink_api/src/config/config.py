"""
Configuration settings for the Starlink Platform API.
"""
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration class."""
    # Flask configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False
    TESTING = False
    
    # JWT configuration
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'default_jwt_secret_key')
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
    JWT_REFRESH_TOKEN_EXPIRES = 2592000  # 30 days
    
    # Database configuration
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('DB_USERNAME', 'postgres')}:{os.getenv('DB_PASSWORD', 'password')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME', 'starlink_platform')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Redis configuration
    REDIS_URL = f"redis://{os.getenv('REDIS_HOST', 'localhost')}:{os.getenv('REDIS_PORT', '6379')}/{os.getenv('REDIS_DB', '0')}"
    
    # Starlink API configuration
    STARLINK_API_URL = os.getenv('STARLINK_API_URL', 'https://web-api.starlink.com')
    STARLINK_CLIENT_ID = os.getenv('STARLINK_CLIENT_ID', '')
    STARLINK_CLIENT_SECRET = os.getenv('STARLINK_CLIENT_SECRET', '')
    
    # Email configuration
    EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.example.com')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', '587'))
    EMAIL_USERNAME = os.getenv('EMAIL_USERNAME', '')
    EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
    EMAIL_USE_TLS = os.getenv('EMAIL_USE_TLS', 'True').lower() == 'true'
    EMAIL_FROM = os.getenv('EMAIL_FROM', 'noreply@example.com')


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"postgresql://{os.getenv('DB_USERNAME', 'postgres')}:{os.getenv('DB_PASSWORD', 'password')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME', 'starlink_platform_test')}"


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False


# Dictionary of configuration environments
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

# Get configuration based on environment
def get_config():
    """Get configuration based on environment."""
    env = os.getenv('FLASK_ENV', 'development')
    return config_by_name.get(env, DevelopmentConfig)

