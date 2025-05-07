from passlib.context import CryptContext


class Crypto:
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def encrypt(self, secret):
        return self.pwd_context.hash(secret)

    def verify(self, plain_secret, hashed_secret):
        return self.pwd_context.verify(plain_secret, hashed_secret)