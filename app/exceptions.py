class AppError(Exception):
    def __init__(self, message: str, status_code: int):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class InvalidCredentials(AppError):
    def __init__(self):
        super().__init__("Invalid credentials", 401)

class EmailAlreadyRegistered(AppError):
    def __init__(self):
        super().__init__("Email already registered", 409)

class EmailNotConfirmed(AppError):
    def __init__(self):
        super().__init__("Email not confirmed", 403)

class UserNotFound(AppError):
    def __init__(self):
        super().__init__("User not found", 403)
        
class OtpExpired(AppError):
    def __init__(self):
        super().__init__("Expired Otp", 403)

class InvalidOtp(AppError):
    def __init__(self):
        super().__init__("Invalid Otp", 403)

class OtpNotFound(AppError):
    def __init__(self):
        super().__init__("Otp not found", 403)
