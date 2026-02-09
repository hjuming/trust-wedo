from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    ALLOWED_ORIGINS: list[str] = ["http://localhost:5173"]
    
    # Supabase
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_KEY: str
    
    class Config:
        env_file = ".env"

print("--- Loading Configuration ---")
import os
print(f"Current Working Directory: {os.getcwd()}")
print(f"Directory Contents: {os.listdir('.')}")
print(f"DATABASE_URL is set: {'DATABASE_URL' in os.environ}")
print(f"SUPABASE_URL is set: {'SUPABASE_URL' in os.environ}")
print("--- End Debug Info ---")

try:
    settings = Settings()
    print("Configuration loaded successfully.")
except Exception as e:
    print(f"!!! Configuration Loading Failed: {e} !!!")
    # 為了避免直接 crash 看不到 log，這裡可以暫時給假資料或 re-raise
    raise e
