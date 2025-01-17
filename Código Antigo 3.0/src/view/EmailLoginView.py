import os
import sys
import time
from src.styles import *
from src.controller.DataUserController import DataUserController
from src.view.EmailMainView import EmailMainView
from PyQt5.QtWidgets import (
    QWidget, 
    QLabel, 
    QLineEdit, 
    QPushButton, 
    QVBoxLayout,
    QMessageBox,
    QDesktopWidget,
    QCheckBox,
    QHBoxLayout,
    )
from PyQt5.QtCore import Qt

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(
        os.path.abspath(__file__)))
   
    return os.path.join(base_path, relative_path)


def limpar_tela():
    time.sleep(3)
    os.system('cls' if os.name == "nt" else "clear")
    
    
class EmailLoginView(QWidget):
    
    def __init__(self):
        super().__init__()
        self.init_ui(styleMain)
        
    def init_ui(self, styleMain):
        # Limpa a tela
        limpar_tela()
        # Define o título da janela
        self.setWindowTitle('Enviar E-mails')
        # Define o estilo CSS da janela
        self.setStyleSheet(styleMain)
        # Desabilita o o botão de maximizar a tela
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowMaximizeButtonHint)
        # Define o tamanho da janela
        self.setGeometry(80, 80, 250, 250)

        self.email_envio_label = QLabel('E-mail de envio:')  # Cria um rótulo para o campo de e-mail
        self.email_envio_edit = QLineEdit()  # Cria um campo de entrada para o e-mail
        self.email_envio_edit.setPlaceholderText('(Utilize um email do Google)')

        self.senha_app_label = QLabel('Senha:')  # Cria um rótulo para o campo de senha
        self.senha_app_edit = QLineEdit()  # Cria um campo de entrada para a senha
        self.senha_app_edit.setPlaceholderText('(Utilize uma senha de app do google)')
        self.senha_app_edit.setEchoMode(QLineEdit.Password)  # Configura o campo de senha para ocultar a entrada
        
        self.info_senha_app = QLabel()
        self.info_senha_app.setText('<a href="https://support.google.com/accounts/answer/185833">O que é uma senha de app?</a>')
        self.info_senha_app.setOpenExternalLinks(True)

        self.show_password_button = QCheckBox('Mostrar Senha')  # Cria um botão de seleção para mostrar a senha
        self.show_password_button.stateChanged.connect(self.toggle_echo_mode)
        
        self.button_login = QPushButton('Logar')  # Cria um botão para efetuar o login
        self.button_login.setStyleSheet(f'background-color: {cor_azul_escuro}')
        self.button_login.clicked.connect(self.check_data_user)
        
        self.button_modificar_dados = QPushButton('Modificar Dados')  # Cria um botão para efetuar modificação de dados
        self.button_modificar_dados.clicked.connect(self.update_data_user)
        
        self.button_criar_conta = QPushButton('Criar Conta')  # Cria um botão para criar uma conta
        self.button_criar_conta.clicked.connect(self.create_data_user)
        
        layout = QVBoxLayout()
        layout.addWidget(self.email_envio_label)
        layout.addWidget(self.email_envio_edit)
        layout.addWidget(self.senha_app_label)
        layout.addWidget(self.senha_app_edit)
        layout.addWidget(self.info_senha_app)
        layout.addWidget(self.show_password_button)
        layout.addWidget(self.button_login)
        
        layout_buttons = QHBoxLayout()
        layout_buttons.addWidget(self.button_modificar_dados)
        layout_buttons.addWidget(self.button_criar_conta)
        
        layout.addLayout(layout_buttons)

        self.setLayout(layout)
        self.show()
        self.center_window()
        
        
    def center_window(self):
        # Obtém a geometria da tela principal
        screen = QDesktopWidget().screenGeometry()

        # Obtém a geometria da própria janela
        window = self.geometry()

        # Calcula a posição x e y para centralizar a janela
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2

        # Define a posição da janela para centralizá-la
        self.move(x, y)
        
        
    def verify_data_user(self) -> bool:
        if not self.email_envio_edit.text() or not self.senha_app_edit.text():
            # Retorna False e exibe uma mensagem de erro se algum campo estiver vazio
            QMessageBox.warning(self, 'Campos Vazios', 'Por favor, preencha o e-mail remetente e a senha.')
            return False
        
        if '@' not in self.email_envio_edit.text() or '.com' not in self.email_envio_edit.text():
            # Retorna False e exibe uma mensagem de erro se o e-mail for inválido
            QMessageBox.warning(self, 'E-mail Inválido', 'Por favor, digite um e-mail válido.')
            return False
        
        return True
        
        
    def toggle_echo_mode(self, state) -> None:
        # Alterna entre mostrar ou ocultar caracteres na entrada de senha com base no estado da caixa de seleção
        if state == Qt.Checked:
            # Se a caixa de seleção estiver marcada, mostra os caracteres
            self.senha_app_edit.setEchoMode(QLineEdit.Normal)
        else:
            # Se a caixa de seleção não estiver marcada, oculta os caracteres
            self.senha_app_edit.setEchoMode(QLineEdit.Password)
            
            
    def open_main_view(self, email: str, app_password: str) -> None:
        self.main_view = EmailMainView(email, app_password)
        self.main_view.show()
            
            
    def create_data_user(self) -> None:
        if not self.verify_data_user():
            return
        
        email: str = self.email_envio_edit.text().strip()
        app_password: str = self.senha_app_edit.text().strip()
        
        try:
            DataUserController(
                email = email,
                app_password = app_password    
            ).save_data_in_json()
    
            QMessageBox.information(self, 'Sucesso', 'Conta criada com sucesso!')
        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Erro ao criar conta: {str(e)}')
            
    
    def update_data_user(self) -> None:
        if not self.verify_data_user():
            return
        
        email: str = self.email_envio_edit.text().strip()
        app_password: str = self.senha_app_edit.text().strip()
        
        try:
            DataUserController(
                email = email,
                app_password = app_password    
            ).update_data_in_json()
    
            QMessageBox.information(self, 'Sucesso', 'Dados atualizados com sucesso!')
        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Erro ao criar conta: {str(e)}')
            
    
    def check_data_user(self) -> None:
        if not self.verify_data_user():
            return
        
        email: str = self.email_envio_edit.text().strip()
        app_password: str = self.senha_app_edit.text().strip()
        
        try:
            data_user_controller: DataUserController = DataUserController(
                email = email,
                app_password = app_password    
            )
            
            if not data_user_controller.check_data_user():
                QMessageBox.critical(self, 'Erro', 'Credênciais inválidas!')
                return
    
            QMessageBox.information(self, 'Sucesso', 'Login realizado com sucesso!')
            self.open_main_view(email, app_password)
            self.close()
        except Exception as e:
            QMessageBox.critical(self, 'Erro', f'Erro ao verificar credenciais: {str(e)}')