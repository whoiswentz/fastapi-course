import passlib
from passlib.context import CryptContext

crypt_context = CryptContext(schemes='bcrypt', deprecated="auto")


class Hash:
    def bcrypt(password: str) -> str:
        return crypt_context.hash(password)

    def verify(hashed_password: str, plain_password: str) -> bool:
        return crypt_context.verify(plain_password, hashed_password)
