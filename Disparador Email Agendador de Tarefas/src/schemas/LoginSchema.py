from dataclasses import dataclass

@dataclass
class LoginSchema:
    email: str
    app_password: str