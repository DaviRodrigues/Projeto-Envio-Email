from src.controllers.SenderEmailController import SenderEmailController
from src.schemas.LoginSchema import LoginSchema
from src.utils.ColoramaUtils import rand_color, Style

class EmailSender:
    def __init__(self, dataSenderEmail: dict, dataUserController: LoginSchema):
        self.dataSenderEmail = dataSenderEmail
        self.dataUserController = dataUserController
        self.colorTerminal = rand_color()
        
    def requisicao_iniciar_envios(self) -> None:    
        try:
            print(f"{self.colorTerminal}Iniciando envio de emails do email {self.dataUserController.email}... {Style.RESET_ALL}\n")
                
            SenderEmailController(
                data_user = self.dataUserController, 
                data_send = self.dataSenderEmail,
                colorTerminal = self.colorTerminal,
            ).send_emails()

            print(f"{self.colorTerminal}Finalizado envio de emails do emails {self.dataUserController.email}!{Style.RESET_ALL}")
        except Exception as e:
            print(f'{self.colorTerminal}Erro ao iniciar o envio de e-mails: {str(e)}{Style.RESET_ALL}')