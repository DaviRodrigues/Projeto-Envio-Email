from src.controller.DataUserController import DataUserController
from pydantic import BaseModel, Field
from typing import Optional

class SenderEmailModel(BaseModel):
    data_user: DataUserController
    data_send: dict = Field(..., description="Dados de envio de e-mail")
    list_columns: Optional[list[str]] = Field(..., description="Lista de colunas da planilha")
    
    class Config:
        from_attributes = True
    