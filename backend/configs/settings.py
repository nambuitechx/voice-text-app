from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(extra="ignore")

    ENV: str = "dev"
    
    AWS_REGION: str = "ap-southeast-1"
    
    DB_NAME: str
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASSWORD: str
    
    # TENANT_ID: str = "d0e22dff-ab2a-4be0-b88f-7880813a2ea2"
    # CLIENT_ID: str = "0da0e7ad-776a-49f9-9d4f-a5cc74d94d81"
    # MASTER_ADMIN_EMAILS: str = "nam.bui@techxcorp.com,vi.diep@techxcorp.com"

settings = Settings(_env_file=".env")
