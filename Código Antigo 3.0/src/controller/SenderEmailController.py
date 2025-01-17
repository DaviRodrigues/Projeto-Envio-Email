import random
import time
import smtplib
import pandas as pd
from PyQt5.QtCore import pyqtBoundSignal
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from smtplib import SMTPException, SMTPAuthenticationError, SMTPConnectError, SMTPServerDisconnected, SMTPRecipientsRefused
from src.controller.DataUserController import DataUserController
from src.model.SenderEmailModel import SenderEmailModel
from src.log.Log import Log

class SenderEmailController(SenderEmailModel):
    
    @staticmethod
    def clean_text(text: str) -> str:
        return text.replace('\xa0', ' ').encode('ascii', 'ignore').decode('ascii')
    
    
    @staticmethod
    def load_html(corpo_email_path: str):
        with open(corpo_email_path, "r", encoding="utf-8") as file:
            return file.read()
        
    
    @staticmethod
    def wait_random_send_email(send_interval: int) -> int:
        return random.randint(send_interval - 5, send_interval + 5)
    
    
    @staticmethod
    def is_file_locked(file_path: str) -> bool:
        try:
            with open(file_path, 'r+'):
                return False
        except OSError:
            return True
    
    
    def __init__(self, data_user: DataUserController, spreadsheet_path: str, html_path: str, email_send_quantity: int, send_interval: int, email_subject: str, email_title: str, email_message: str, whatsapp_redirect_number: str, redirect_message: str):
        super().__init__(
            data_user=data_user,
            spreadsheet_path=spreadsheet_path,
            html_path=html_path,
            email_send_quantity=email_send_quantity, 
            send_interval=send_interval, 
            email_subject=email_subject, 
            email_title=email_title, 
            email_message=email_message, 
            whatsapp_redirect_number=whatsapp_redirect_number,
            redirect_message=redirect_message,
            list_columns=None
        )

    
    def read_emails(self) -> tuple[list[str], pd.DataFrame, list[str]]:
        if SenderEmailController.is_file_locked(self.spreadsheet_path):
            raise Exception("O arquivo de planilha está sendo utilizado por outro processo, feche-a e tente novamente.")
        
        df_emails = pd.read_excel(self.spreadsheet_path, converters={"STATUS": str})
        
        self.list_columns = df_emails.columns.tolist()
        variables_columns: list[str] = list(filter(lambda x: x not in ['E-mail', 'STATUS'], self.list_columns))
        
        try:
            if not {"E-mail", "STATUS"}.issubset(self.list_columns):
                raise KeyError("Coluna 'E-mail' ou 'STATUS' não encontrada na planilha. (Colunas obrigatórias)")
            
            df_no_duplicates: pd.DataFrame = df_emails.drop_duplicates(
                subset=self.list_columns, keep='first')

            df_no_duplicates.to_excel(self.spreadsheet_path, index=False)
            
            colum_emails: list[str] = df_no_duplicates["E-mail"].tolist()

            return colum_emails, df_no_duplicates, variables_columns
        except Exception as error:
            raise Exception(f"Erro ao carregar emails: {error}")
    
    
    def verify_last_index_and_start_index(self, df_emails: pd.DataFrame) -> int:
        last_sent_index: int = df_emails[df_emails["STATUS"].isin(['ENVIADO', 'ERRO'])].index.max()
        return(last_sent_index + 1) if pd.notna(last_sent_index) else 0
    
    
    def get_values_of_spreadsheet(self, df_emails: pd.DataFrame, variables_columns: list[str], index: int) -> dict[str, str]:
        def has_value(value: str) -> str:
            return '' if value == 'nan' or value is None else value
        
        dynamic_values: dict[str, str] = {
            column: has_value(str(df_emails.loc[index, column]))
            for column in variables_columns
        }
        
        return dynamic_values
    

    def update_message(self, columns_values: dict[str, str]) -> tuple[str, str, str]:
        message_copy: str = self.email_message
        title_copy: str = self.email_title
        
        for key, value in columns_values.items():
            message_copy = message_copy.replace(f"{{{key.lower()}}}", value)
            title_copy = title_copy.replace(f"{{{key.lower()}}}", value)
                
        link_whatsapp_copy: str = f"https://api.whatsapp.com/send?phone={self.whatsapp_redirect_number}&text={self.redirect_message}"

        return message_copy, title_copy, link_whatsapp_copy
    
    
    def type_verify_email(self) -> tuple[str, int]:
        email_and_server: dict[str, str] = {
            "gmail.com": ("smtp.gmail.com", 587),
            "webcertificados.com.br": ("smtp.gmail.com", 587),
            "webcertificado.com.br": ("smtp.gmail.com", 587),
            "outlook.com": ("smtp.office365.com", 587),
            "hotmail.com": ("smtp.live.com", 587),
            "aol.com": ("smtp.aol.com", 587),
            "icloud.com": ("smtp.mail.me.com", 587),
        }
        
        domain: str = self.data_user.email.split('@')[-1]

        return email_and_server.get(domain, "smtp.gmail.com")  
    
    
    def config_send_email(self, destination_email: str, copy_body_html: str) -> None:
        server_smtp, port_smtp = self.type_verify_email()
        
        msg = MIMEMultipart('alternative')
        msg['Subject'] = self.email_subject
        msg['From'] = self.data_user.email
        msg['To'] = destination_email
        msg.attach(MIMEText(copy_body_html, 'html', 'utf-8'))
        
        with smtplib.SMTP(server_smtp, port_smtp) as server:
            server.starttls()
            server.login(msg['From'], self.clean_text(self.data_user.app_password))
            server.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
            

    def replace_email_html(self, body_html_original: str, message_copy: str, title_copy: str, link_whatsapp_copy: str) -> str:
        copy_body_html: str = body_html_original
        copy_body_html = copy_body_html.replace('{titulo_html}', title_copy)
        copy_body_html = copy_body_html.replace('{mensagem_html}', message_copy)
        copy_body_html = copy_body_html.replace('{link_whatsapp}', link_whatsapp_copy)
        
        return copy_body_html
    
    
    def write_on_console_and_txt(self, destination_email: str, destination_emails: list[str], validator: bool, index: int, start_index: int=None, error: str=None, interval_send_email: int=None) -> str:
        if not validator:
            message: str = f"Erro ao enviar email para {destination_email} às {datetime.now().strftime('%d/%m/%Y-%H:%M:%S')}. Erro: {error}\n"
            Log.write_error(self.data_user.email, message)
            return message
        
        message: str = f"Email enviado para {destination_email} às {datetime.now().strftime('%d/%m/%Y-%H:%M:%S')}\nTotal de emails enviados: {index + 1} de {len(destination_emails[start_index:])} " + f"Intervalo de envio: {interval_send_email} segundos\n"
        Log.write_success(self.data_user.email, message)
        return message
    
    
    def pre_process_emails(self, df_emails: pd.DataFrame, destination_email: str, body_html_original: str, variables_columns: list[str], index: int) -> list[str]:
        columns_values: dict[str, str] = self.get_values_of_spreadsheet(df_emails, variables_columns, index)
        message_copy, title_copy, link_whatsapp_copy = self.update_message(columns_values)
        copy_body_html: str = self.replace_email_html(body_html_original, message_copy, title_copy, link_whatsapp_copy)
        self.config_send_email(destination_email, copy_body_html)
        
    
    def sucess_env(self, df_emails: pd.DataFrame, destination_email: str, destination_emails: list[str], index: int, start_index: int, random_interval: int, log_signal: pyqtBoundSignal) -> None:
        df_emails.loc[index, "STATUS"] = 'ENVIADO'
        df_emails.to_excel(self.spreadsheet_path, index=False)
        message_success: str = self.write_on_console_and_txt(destination_email, destination_emails, True, index, start_index, None, random_interval)
        log_signal.emit(message_success)
        time.sleep(random_interval)
    
    
    def error_env(self, df_emails: pd.DataFrame, destination_email: str, destination_emails: list[str], index: int, error: Exception, log_signal: pyqtBoundSignal) -> None:
        df_emails.loc[index, "STATUS"] = 'ERRO'
        df_emails.to_excel(self.spreadsheet_path, index=False)
        message_error: str = self.write_on_console_and_txt(destination_email, destination_emails, False, index, None, error, None)
        log_signal.emit(message_error)
        
    
    def send_emails(self, log_signal: pyqtBoundSignal) -> None:
        body_html_original: str = SenderEmailController.load_html(self.html_path)
        destination_emails, df_emails, variables_columns = self.read_emails()
        
        start_index: int = self.verify_last_index_and_start_index(df_emails)
        
        if not destination_emails or not destination_emails[start_index:]:
            raise Exception("Nenhum e-mail encontrado na planilha para envio. Cheque a coluna de E-mail ou STATUS.")
        
        for index, destination_email in enumerate(destination_emails[start_index:]):
            random_interval: int = SenderEmailController.wait_random_send_email(self.send_interval)
            if (index + 1) > self.email_send_quantity:
                break
            
            try:
                self.pre_process_emails(df_emails, destination_email, body_html_original, variables_columns, index)
                self.sucess_env(df_emails, destination_email, destination_emails, index, start_index, random_interval, log_signal)
            except SMTPAuthenticationError:
                message_error: str = "Erro de autenticação ou limite de envios excedido. Verifique o e-mail e senha do aplicativo., ou contate o suporte."
                self.error_env(df_emails, destination_email, destination_emails, index, message_error, log_signal)
                break
            except SMTPRecipientsRefused:
                message_error: str = f"O e-mail {destination_email} foi recusado pelo servidor SMTP. Tente iniciar os envios novamente ou feche o programa."
                self.error_env(df_emails, destination_email, destination_emails, index, message_error, log_signal)
                continue
            except (SMTPConnectError, SMTPServerDisconnected):
                message_error: str = "Conexão ou Falha com o servidor SMTP. Tente iniciar os envios novamente ou feche o programa."
                self.error_env(df_emails, destination_email, destination_emails, index, message_error, log_signal)
                break
            except Exception as error:
                self.error_env(df_emails, destination_email, destination_emails, index, error, log_signal)
                continue

