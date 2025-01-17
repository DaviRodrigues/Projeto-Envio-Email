from src.model.DataUserModel import DataUserModel
import os
import sys
import json

class DataUserController(DataUserModel):
    
    @staticmethod
    def resource_path(relative_path):
        base_path: None | str = getattr(sys, '_MEIPASS', os.path.dirname(
            os.path.abspath(__file__)))
    
        return os.path.join(base_path, "data", relative_path)
    
    def __init__(self, email: str, app_password: str):
        super().__init__(archive_name=f"credentials_{email}.json", email=email, app_password=app_password)
    
    def check_data_user(self) -> bool:
        data_user_json = self.__load_data_from_json()
        
        return data_user_json["email"] == self.email and data_user_json["app_password"] == self.app_password
    
    
    def save_data_in_json(self) -> None:
        # Não é a melhor forma de se fazer no momento, pois isso pode acarretar em falha de segurança
        # No caso se alguém ver que o email existe, pode colocar outra senha para esse email e bloquear o acesso de outro usuário
        paste_name: str = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__))) + "\\data"
        if not os.path.exists(paste_name):
            os.mkdir(paste_name)
        
        if os.path.exists(DataUserController.resource_path(self.archive_name)):
            raise Exception("Email já existente, escolha outro!")
                
        with open(DataUserController.resource_path(self.archive_name), "w") as file:
            json.dump({
                "email": self.email,
                "app_password": self.app_password
            }, file)
            
    
    def update_data_in_json(self) -> None:
        if not os.path.exists(DataUserController.resource_path(self.archive_name)):
            raise Exception("Usuário não encontrado!")
        
        data_user: dict[str, str] = self.__load_data_from_json()
        
        if data_user["email"] == self.email and data_user["app_password"] == self.app_password:
            raise Exception("Credenciais inválidas!")
        
        if data_user["email"] != self.email:
            raise Exception("Email inválido!")
            
        with open(DataUserController.resource_path(self.archive_name), "w") as file:
            json.dump({
                "email": data_user["email"],
                "app_password": self.app_password
            }, file)
            
    
    def __load_data_from_json(self) -> dict[str, str]:
        try:
            with open(DataUserController.resource_path(self.archive_name), 'r') as file:
                data_user_json = json.load(file)
        except FileNotFoundError:
            raise FileNotFoundError("Usuário não encontrado! Tente criar um.")

        return data_user_json