from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "mysql+pymysql://root:123456@localhost:3306/xuntian_ops"
    SECRET_KEY: str = "xuntian-ops-secret-key-2026"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 1440

    # Alibaba Cloud
    ALIYUN_ACCESS_KEY_ID: str = ""
    ALIYUN_ACCESS_KEY_SECRET: str = ""
    ALIYUN_REGION: str = "cn-hangzhou"

    class Config:
        env_file = ".env"


settings = Settings()
