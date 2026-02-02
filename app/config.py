import os

LOCAL_DB_PATH = "/Users/smruti/Dev/2mpattanaik/ecommerce_rest_api/local_data/shop.db"
DOCKER_DB_PATH = "/data/shop.db"
SECRET_KEY = "supersecret"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

def running_in_docker() -> bool:
    return os.path.exists("/.dockerenv")

def get_db_path() -> str:
    # 1. Explicit override (CI / prod / power users)
    if os.getenv("DB_PATH"):
        return os.getenv("DB_PATH")

    # 2. Auto-detect Docker
    if running_in_docker():
        return DOCKER_DB_PATH

    # 3. Safe local default
    return LOCAL_DB_PATH
