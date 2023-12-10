from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from . import schemas, models
from .database import get_db
from fastapi.security import OAuth2PasswordBearer
from .config.app_settings import settings

oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login")


def create_access_token(data: schemas.TokenData) -> str:
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode.update({"exp": expire})   

    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt
    

def verify_token(token: str, credentials_exception) -> schemas.TokenData:
    try:
        decoded_token = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: str = decoded_token.get("user_id")
        if user_id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(user_id=user_id)
        return token_data
    except JWTError:
        raise credentials_exception
    
def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not valid credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    id = verify_token(token, credentials_exception).user_id

    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise credentials_exception
    return user
 