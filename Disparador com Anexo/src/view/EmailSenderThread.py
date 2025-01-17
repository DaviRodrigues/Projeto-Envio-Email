import time
from src.controller.DataUserController import DataUserController
from src.controller.SenderEmailController import SenderEmailController
from PyQt5.QtCore import QThread, pyqtSignal, pyqtBoundSignal

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
                self.log_signal.emit('Envio de e-mails iniciado com sucesso!\n')
                
                SenderEmailController(
                    data_user = dataUserController, 
                    data_send = self.data
                ).send_emails(self.log_signal)
                
            self.stop()
        except Exception as e:
            self.log_signal.emit(f'Erro ao iniciar o envio de e-mails: {str(e)}')
            self.stop()
            
            
    def stop(self):
        self.running = False