from passlib.context import CryptContext
from datetime import datetime, timedelta
import jwt
from src.config import Config    
import uuid
import logging
from itsdangerous import URLSafeTimedSerializer

passwd_context = CryptContext(schemes=["bcrypt"]) 

ACCESS_TOKEN_EXPIRY=3600


def generate_password_hash(password: str) -> str:
    hash = passwd_context.hash(password)

    return hash

def verify_password(password: str, hash: str) -> bool:
    return passwd_context.verify(password, hash)


def create_access_token(user_data:dict,expiry:timedelta = None,refresh:bool = False):
    payload={}

    payload['user']= user_data
    payload['exp'] = datetime.now()+ (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))

    payload["jti"]=str(uuid.uuid4())

    payload["refresh"]=refresh
    
    token = jwt.encode(
        payload=payload,
        key=Config.JWT_SECRET,
        algorithm=Config.JWT_ALGORITHM,
    )

    return token

def decode_token(token:str)->dict:
    try:
        token_data=jwt.decode(
            jwt=token,
            key=Config.JWT_SECRET,
            algorithms=[Config.JWT_ALGORITHM]
        )

        return token_data
    except jwt.PyJWKError as e:
        logging.exception(e)
        return None
    
serializer = URLSafeTimedSerializer(
    secret_key=Config.JWT_SECRET,
    salt="email-verification",
)

def create_url_safe_token(data:dict):
    
    token = serializer.dumps(data,salt="email-verification")

    return token

def decode_url_safe_token(token:str):
    try:
        token_data = serializer.loads(token)
        
        return token_data
    except Exception as e:
        logging.error(str(e))