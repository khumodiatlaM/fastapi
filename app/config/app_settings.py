from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Social Media API"
    
    # Database
    database_hostname: str 
    database_port: str
    database_username: str 
    database_password: str 
    database_name: str

    # JWT
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"
    
settings = Settings()