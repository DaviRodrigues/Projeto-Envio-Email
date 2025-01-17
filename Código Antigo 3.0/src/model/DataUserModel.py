from pydantic import BaseModel, Field, EmailStr

class DataUserModel(BaseModel):
    archive_name: str = Field(..., description="Nome do arquivo")
    email: EmailStr = Field(..., description="Email do usuário")
    app_password: str = Field(..., description="Senha do usuário")
    
    class Config:
        from_attributes = True
    