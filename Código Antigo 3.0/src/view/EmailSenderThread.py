import time
from src.controller.DataUserController import DataUserController
from src.controller.SenderEmailController import SenderEmailController
from PyQt5.QtCore import QThread, pyqtSignal

class EmailSenderThread(QThread):
    log_signal = pyqtSignal(str)
    finished_signal = pyqtSignal()

    def __init__(self, data: dict, parent=None):
        super().__init__(parent)
        self.data = data
        self.running = True

    def run(self):
        try:
            while self.running:
                self.requisicao_iniciar_envios()
                time.sleep(self.data["send_interval"])    
            return
        except Exception as e:
            self.log_signal.emit(f'Erro ao tentar obter logs: {str(e)}')
            return
        finally:
            self.finished_signal.emit()
        
        
    def requisicao_iniciar_envios(self) -> None:    
        try:
            dataUserController: DataUserController = DataUserController(
                email = self.data["email"],
                app_password = self.data["app_password"]
            )
            
            validator: bool = dataUserController.check_data_user()
            
            if validator:
                self.log_signal.emit("Iniciando envio de e-mails...\n")
                
                SenderEmailController(
                    data_user = dataUserController, 
                    spreadsheet_path = self.data["spreadsheet_path"],
                    html_path = self.data["html_path"],
                    email_send_quantity = self.data["email_send_quantity"],
                    send_interval = self.data["send_interval"],
                    email_subject = self.data["email_subject"],
                    email_title = self.data["email_title"],
                    email_message = self.data["email_message"],
                    whatsapp_redirect_number = self.data["whatsapp_redirect_number"],
                    redirect_message=self.data["redirect_message"] 
                ).send_emails(self.log_signal)
                
            self.stop()
        except Exception as e:
            self.log_signal.emit(f'Erro no o envio de e-mails: {str(e)}')
            self.stop()
            
            
    def stop(self):
        self.running = False