from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash(password: str):
    # hash the password
    return pwd_context.hash(password)

def verify(password: str, hashed_password: str):
    # verify the password
    return pwd_context.verify(password, hashed_password)
