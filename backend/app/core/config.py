from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "sqlite:///./faithschool.db"
    
    # Security
    SECRET_KEY: str = "dev-secret-key-change-in-production-min-32-chars-long"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Environment
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    ALLOWED_ORIGINS: str = "http://localhost:5174,http://localhost:5173,http://127.0.0.1:5174,file://"
    
    # Email
    SENDGRID_API_KEY: str = ""
    FROM_EMAIL: str = "noreply@faithschool.rw"
    FROM_NAME: str = "Faith Brilliant Stars School"
    
    # SMS
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_PHONE_NUMBER: str = ""
    SMS_PROVIDER: str = "twilio"
    
    # Firebase
    FIREBASE_CREDENTIALS_PATH: str = ""
    
    # Mobile Money
    MTN_MOMO_API_KEY: str = ""
    MTN_MOMO_USER_ID: str = ""
    MTN_MOMO_SUBSCRIPTION_KEY: str = ""
    AIRTEL_MONEY_CLIENT_ID: str = ""
    AIRTEL_MONEY_CLIENT_SECRET: str = ""
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379/0"
    
    # Sentry
    SENTRY_DSN: str = ""
    
    # School
    SCHOOL_NAME: str = "Faith Brilliant Stars School"
    SCHOOL_PHONE: str = "+250XXXXXXXXX"
    SCHOOL_EMAIL: str = "info@faithschool.rw"
    SCHOOL_ADDRESS: str = "Kigali, Rwanda"
    CURRENCY: str = "RWF"
    DEFAULT_LANGUAGE: str = "en"
    SUPPORTED_LANGUAGES: str = "en,rw"
    
    # File Upload
    MAX_UPLOAD_SIZE_MB: int = 10
    UPLOAD_DIR: str = "./uploads"
    
    @property
    def origins_list(self) -> List[str]:
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",")]
    
    @property
    def languages_list(self) -> List[str]:
        return [lang.strip() for lang in self.SUPPORTED_LANGUAGES.split(",")]
    
    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        case_sensitive = True
        extra = 'ignore'

settings = Settings()
