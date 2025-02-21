import sys
import webbrowser
import os
import time
from src.styles import *
from src.view.EmailSenderThread import EmailSenderThread
from datetime import datetime
from PyQt5.QtWidgets import (
    QWidget, 
    QLabel, 
    QLineEdit, 
    QPushButton, 
    QVBoxLayout, 
    QFileDialog, 
    QMessageBox, 
    QTextEdit, 
    QDesktopWidget, 
    QHBoxLayout,
    )
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIntValidator

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(
        os.path.abspath(__file__)))
   
    return os.path.join(base_path, relative_path)


def limpar_tela():
    time.sleep(3)
    os.system('cls' if os.name == "nt" else "clear")


class EmailMainView(QWidget):
    
    def __init__(self, email: str, app_password: str):
        super().__init__()
        self.init_ui(styleMain)
        self.email = email
        self.app_password = app_password
        self.email_thread = None
        self.log_thread = None
        

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
        self.setGeometry(100, 100, 350, 350)

        self.planilha_path_label = QLabel('Escolha a Planilha:')  # Cria um rótulo para o campo de caminho da planilha
        self.planilha_path_edit = QLineEdit()  # Cria um campo de entrada para o caminho da planilha
        self.planilha_path_edit.setReadOnly(False)  # Configura o campo de caminho da planilha para ser somente leitura
        self.planilha_path_edit.setPlaceholderText('.xlsx')  # Define um texto de espaço reservado para o campo de caminho da planilha

        self.choose_planilha_button = QPushButton('Escolher')  # Cria um botão para escolher a planilha
        self.choose_planilha_button.clicked.connect(self.choose_planilha)
        
        self.html_path_label = QLabel('Escolha o corpo HTML email:')  # Cria um rótulo para o campo de caminho do HTML
        self.html_path_edit = QLineEdit()  # Cria um campo de entrada para o caminho do HTML
        self.html_path_edit.setReadOnly(False)  # Configura o campo de caminho do HTML para ser somente leitura
        self.html_path_edit.setPlaceholderText('.html')  # Define um texto de espaço reservado para o campo de caminho do HTML

        self.choose_html_button = QPushButton('Escolher')  # Cria um botão para escolher o corpo HTML
        self.choose_html_button.clicked.connect(self.choose_html)
        
        self.baixar_planilha = QPushButton('Baixar Planilha Base')  # Cria um botão para baixar a planilha base
        self.baixar_planilha.clicked.connect(self.baixar_planilha_base)  # Conecta o botão de download a uma função para baixar a planilha base

        self.numero_envios_label = QLabel('Número de Envios:')  # Cria um rótulo para o campo de número de envios
        self.numero_envios_edit = QLineEdit()  # Cria um campo de entrada para o número de envios
        self.numero_envios_edit.setMaxLength(10)
        self.numero_envios_edit.setValidator(QIntValidator())
        self.numero_envios_edit.setPlaceholderText('Nº')  # Define um texto de espaço reservado para o campo de número de envios

        self.intervalo_envio_label = QLabel('Intervalo entre Envios (segundos):')  # Cria um rótulo para o campo de intervalo entre envios
        self.intervalo_envio_edit = QLineEdit()  # Cria um campo de entrada para o intervalo entre envios
        self.intervalo_envio_edit.setMaxLength(10)
        self.intervalo_envio_edit.setValidator(QIntValidator())
        self.intervalo_envio_edit.setPlaceholderText('10')  # Define um texto de espaço reservado para o campo de intervalo entre envios

        self.assunto_label = QLabel('Assunto:')  # Cria um rótulo para o campo de assunto
        self.assunto_edit = QLineEdit()  # Cria um campo de entrada para o assunto
        self.assunto_edit.setPlaceholderText('Assunto do E-mail')  # Define um texto de espaço reservado para o campo de assunto

        self.titulo_html_label = QLabel('Título:')  # Cria um rótulo para o campo de título
        self.titulo_html_edit = QLineEdit()  # Cria um campo de entrada para o título
        self.titulo_html_edit.setPlaceholderText('Título do E-mail')  # Define um texto de espaço reservado para o campo de título
        
        self.limpar_logs_button = QPushButton('Limpar Logs')
        self.limpar_logs_button.clicked.connect(self.limpar_logs)
        
        self.mensagem_html_label = QLabel('Mensagem:')  # Cria um rótulo para o campo de mensagem
        self.mensagem_html_edit = QTextEdit()  # Cria um campo de entrada para a mensagem
        self.mensagem_html_edit.setPlaceholderText('Mensagem principal do E-mail')  # Define um texto de espaço reservado para o campo de mensagem
        
        self.redirecionar_whatsapp_label = QLabel('Número para redirecionar:')
        self.redirecionar_whatsapp_edit = QLineEdit()
        self.redirecionar_whatsapp_edit.setPlaceholderText('O número precisa ser exatamente igual o do whatsapp')
        self.redirecionar_whatsapp_edit.textChanged.connect(self.validateRedirectNumber)
        
        self.mensagem_redirecionar_label = QLabel('Mensagem para redirecionar:')
        self.mensagem_redirecionar_edit = QLineEdit()
        self.mensagem_redirecionar_edit.setPlaceholderText('Mensagem para redirecionar')
        
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)

        self.iniciar_button = QPushButton('Iniciar Envio')  # Cria um botão para iniciar o envio
        self.iniciar_button.setStyleSheet(f'background-color: {cor_azul_escuro}')  # Define o estilo do botão de início
        self.iniciar_button.clicked.connect(self.iniciar_envio)

        
        layout_escolher_planilha = QHBoxLayout() # Adiciona o botão de escolha da planilha ao layout
        layout_escolher_planilha.addWidget(self.planilha_path_label) # Adiciona o rótulo de caminho da planilha ao layout
        layout_escolher_planilha.addWidget(self.planilha_path_edit)  # Adiciona o campo de caminho da planilha ao layout
        layout_escolher_planilha.addWidget(self.choose_planilha_button)  # Adiciona o botão de escolha da planilha ao layout
        
        layout_escolher_html = QHBoxLayout() # Adiciona o botão de escolha do template HTML ao layout
        layout_escolher_html.addWidget(self.html_path_label)  # Adiciona o rótulo de caminho do HTML ao layout
        layout_escolher_html.addWidget(self.html_path_edit)  # Adiciona o campo de caminho do HTML ao layout
        layout_escolher_html.addWidget(self.choose_html_button)  # Adiciona o botão de escolha do HTML ao layout

        layout_baixar_planilha = QHBoxLayout() # Adiciona o botão de escolha da planilha ao layout
        layout_baixar_planilha.addWidget(self.baixar_planilha)  # Adiciona o botão de download da planilha ao layout
        
        layout_intervalo_env = QHBoxLayout()
        layout_intervalo_env.addWidget(self.numero_envios_label)  # Adiciona o rótulo de número de envios ao layout
        layout_intervalo_env.addWidget(self.numero_envios_edit)  # Adiciona o campo de número de envios ao layout
        layout_intervalo_env.addWidget(self.intervalo_envio_label) # Adiciona widgets relacionados ao intervalo entre envios ao layout
        layout_intervalo_env.addWidget(self.intervalo_envio_edit) # Adiciona widgets relacionados ao intervalo entre envios ao layout

        layout_assunto_titulo = QHBoxLayout()
        layout_assunto_titulo.addWidget(self.assunto_label)  # Adiciona o rótulo de assunto ao layout
        layout_assunto_titulo.addWidget(self.assunto_edit)  # Adiciona o campo de assunto ao layout
        layout_assunto_titulo.addWidget(self.titulo_html_label)  # Adiciona o rótulo de título ao layout
        layout_assunto_titulo.addWidget(self.titulo_html_edit)  # Adiciona o campo de título ao layout
        
        layout_redirecionar_whatsapp = QVBoxLayout()
        layout_redirecionar_whatsapp.addWidget(self.redirecionar_whatsapp_label)
        layout_redirecionar_whatsapp.addWidget(self.redirecionar_whatsapp_edit)
        layout_redirecionar_whatsapp.addWidget(self.mensagem_redirecionar_label)
        layout_redirecionar_whatsapp.addWidget(self.mensagem_redirecionar_edit)
        
        layout_limpar_logs_iniciar_button = QHBoxLayout()
        layout_limpar_logs_iniciar_button.addWidget(self.limpar_logs_button)
        layout_limpar_logs_iniciar_button.addWidget(self.iniciar_button)
        
        layout = QVBoxLayout()  # Cria um layout vertical
        
        layout.addLayout(layout_escolher_planilha)
        layout.addLayout(layout_escolher_html)
        layout.addLayout(layout_baixar_planilha)
        
        layout.addLayout(layout_intervalo_env)
        
        layout.addLayout(layout_assunto_titulo)  # Adiciona os campos de assunto e título ao layout
        layout.addWidget(self.mensagem_html_label)  # Adiciona o rótulo de mensagem ao layout
        layout.addWidget(self.mensagem_html_edit)  # Adiciona o campo de mensagem ao layout
        layout.addLayout(layout_redirecionar_whatsapp) # Adiciona o campo de numero e mensagem de redirecionamento ao layout
        
        layout.addWidget(QLabel('Logs:'))
        layout.addWidget(self.log_area)
        
        # Adicione os botões de inserir nome e produto ao layout principal
        # layout.addLayout(layout_nome_e_prod_prot)
        layout.addLayout(layout_limpar_logs_iniciar_button)

        # Adicione o layout principal à janela
        self.setLayout(layout)
        self.show()
        self.center_window()
        
        
    def center_window(self) -> None:
        # Obtém a geometria da tela principal
        screen = QDesktopWidget().screenGeometry()

        # Obtém a geometria da própria janela
        window = self.geometry()

        # Calcula a posição x e y para centralizar a janela
        x = (screen.width() - window.width()) // 2
        y = (screen.height() - window.height()) // 2

        # Define a posição da janela para centralizá-la
        self.move(x, y)
    
    
    def iniciar_envio(self) -> None:
        # Verificar se todos os campos estão preenchidos
        if not self.campos_preenchidos():
            return
            
        QMessageBox.information(self, 'Envio Iniciado', f'Iniciando envio de e-mails dia {datetime.now().strftime("%d")} às {datetime.now().strftime("%H:%M:%S")}')

        self.set_widgets_enabled(False)

        mensagem_html = self.mensagem_html_edit.toPlainText()
        mensagem_html = mensagem_html.replace('\n', '<br>')

        # Verifica se o intervalo de envio é menor que 30 segundos
        if int(self.intervalo_envio_edit.text()) < 10:
            QMessageBox.warning(self, 'Valor Inválido', 'O intervalo entre envios deve ser no mínimo 10 segundos.')
            self.set_widgets_enabled(True)
            return
        
        self.montar_dados_iniciar_thread(mensagem_html)
        
        
    def iniciar_thread_logs(self, data: dict[str, str | int]) -> None:
        self.log_thread = EmailSenderThread(data)
        self.log_thread.log_signal.connect(self.atualizar_logs)
        self.log_thread.finished.connect(self.finalizar_envio)
        self.log_thread.start()
        self.set_widgets_enabled(False)


    def finalizar_envio(self):
        self.set_widgets_enabled(True)
        QMessageBox.information(self, 'Sucesso', 'Envio de e-mails encerrado!')


    def atualizar_logs(self, log_message) -> None:
        self.log_area.append(log_message)
        
    
    def limpar_logs(self) -> None:
        self.log_area.clear()


    def closeEvent(self, event) -> None:
        if self.log_thread is not None:
            self.log_thread.stop()
        event.accept()
    
    
    def montar_dados_iniciar_thread(self, mensagem_html: str) -> None:
        data: dict[str, str | int] = {
            "email": self.email, 
            "app_password": self.app_password,
            "spreadsheet_path": self.planilha_path_edit.text(),
            "html_path": self.html_path_edit.text(),
            "email_send_quantity": int(self.numero_envios_edit.text()),
            "send_interval": int(self.intervalo_envio_edit.text()),
            "email_subject": self.assunto_edit.text(),
            "email_title": self.titulo_html_edit.text(),
            "email_message": mensagem_html,
            "whatsapp_redirect_number": self.redirecionar_whatsapp_edit.text(),
            "redirect_message": self.mensagem_redirecionar_edit.text()
        }
        
        self.iniciar_thread_logs(data)


    def campos_preenchidos(self) -> bool:
        # Lista de campos a serem verificados
        campos: list[tuple[str, str]] = [
            ('Caminho da Planilha', self.planilha_path_edit.text()),
            ('Caminho do HTML', self.html_path_edit.text()),
            ('Número de Envios', self.numero_envios_edit.text()),
            ('Intervalo entre Envios (segundos)', self.intervalo_envio_edit.text()),
            ('Assunto', self.assunto_edit.text()),
            ('Título', self.titulo_html_edit.text()),
            ('Mensagem', self.mensagem_html_edit.toPlainText()),
            ('Número para redirecionar', self.redirecionar_whatsapp_edit.text()),
            ('Mensagem de redirecionamento', self.mensagem_redirecionar_edit.text()),
        ]

        # Itera sobre os campos
        for nome_campo, valor_campo in campos:
            if not valor_campo:
                # Exibe uma mensagem de erro se algum campo estiver vazio
                QMessageBox.warning(self, f'{nome_campo} Vazio', f'Por favor, preencha o campo {nome_campo}.')
                return False

        # Retorna True se todos os campos estiverem preenchidos corretamente
        return True


    def set_widgets_enabled(self, enabled: bool) -> None:
        # Desabilita ou habilita os widgets com base no parâmetro 'enabled'
        lista_desabilitar_ou_habilitar: list = [
            self.baixar_planilha,
            self.planilha_path_edit,
            self.html_path_edit,
            self.choose_html_button,
            self.choose_planilha_button,
            self.numero_envios_edit,
            self.assunto_edit,
            self.titulo_html_edit,
            self.iniciar_button,
            self.mensagem_html_edit,
            self.intervalo_envio_edit,
            self.limpar_logs_button,
            self.redirecionar_whatsapp_edit,
            self.mensagem_redirecionar_edit,
        ]
        
        for _, item in enumerate(lista_desabilitar_ou_habilitar):
            item.setEnabled(enabled)
       
       
    def validateRedirectNumber(self) -> None:
        text: str = self.redirecionar_whatsapp_edit.text()

        text = ''.join(filter(str.isdigit, text))

        if len(text) > 13:
            text = text[:13]

        self.redirecionar_whatsapp_edit.setText(text)   
            

    def choose_planilha(self) -> None:
        # Abre um diálogo para escolher a planilha
        planilha_path, _ = QFileDialog.getOpenFileName(self, 'Escolher Planilha', '', 'Excel Files (*.xlsx *.xls *.csv *.xlsm)')
        if planilha_path:
            self.planilha_path_edit.setText(planilha_path)
            
            
    def choose_html(self) -> None:
        # Abre um diálogo para escolher o arquivo HTML
        html_path, _ = QFileDialog.getOpenFileName(self, 'Escolher Arquivo HTML', '', 'HTML Files (*.html)')
        if html_path:
            self.html_path_edit.setText(html_path)
       
        
    def baixar_planilha_base(self) -> None:
        # Abre o Google para baixar a planilha base através do link de download direto
        webbrowser.open(
            "https://www.dropbox.com/scl/fi/86uil93uepe3sssd7yxm8/Enviar-E-mails.xlsx?rlkey=inogq1zqcm3xjame930yksm75&dl=1"
        )