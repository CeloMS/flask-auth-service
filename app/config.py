import os
from dotenv import load_dotenv

class Settings:

    def __init__(self):
        load_dotenv()

        self.JWT_SECRET = os.getenv("JWT_SECRET", "DEFAULT_VALUE")
        self.JWT_EXPTIME = int(os.getenv("JWT_EXPTIME", 24))
        self.OTP_LENGTH = int(os.getenv("OTP_LENGTH", 6))
        self.OTP_DURATION = int(os.getenv("OTP_DURATION", 10))
        self.OTP_CHARSET = os.getenv("OTP_CHARSET", "1234567890")
        self.GMAIL = os.getenv("GMAIL")
        self.GMAIL_PASSWORD = os.getenv("GMAIL_PASSWORD")

settings = Settings()