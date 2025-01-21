import random
import time
import smtplib
import os
import pandas as pd
from PyQt5.QtCore import pyqtBoundSignal
from datetime import datetime
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from smtplib import SMTPAuthenticationError, SMTPConnectError, SMTPServerDisconnected, SMTPRecipientsRefused
from src.controller.DataUserController import DataUserController
from src.model.SenderEmailModel import SenderEmailModel
from src.log.Log import Log


class SenderEmailController(SenderEmailModel):
    @staticmethod
    def ensure_attachment_directory(directory_path: str) -> None:
        if not os.path.exists(directory_path):
            os.mkdir(directory_path)
            raise FileNotFoundError("A pasta de anexos não foi encontrada. Criando... Coloque os anexos nela.")
    
    
    @staticmethod
    def load_single_attachment(file_path: str) -> MIMEApplication:
        if not os.path.exists(file_path):
            return
        
        with open(file_path, 'rb') as file:
            part: MIMEApplication = MIMEApplication(file.read(), Name=os.path.basename(file_path))
            part['Content-Disposition'] = f'attachment; filename="{os.path.basename(file_path)}"'
            return part


    @staticmethod
    def load_attachments(list_attachments: list[str]) -> list[MIMEApplication] | None:
        attachments_in_memory: list[MIMEApplication] = []
        attachment_path: str = os.getcwd() + "\\anexos"
        
        SenderEmailController.ensure_attachment_directory(attachment_path)

        if not list_attachments:
            return attachments_in_memory

        try:
            for attachment_name in list_attachments:
                file_path: str = f"{attachment_path}\\{attachment_name}"
                attachment: MIMEApplication = SenderEmailController.load_single_attachment(file_path)
                
                if attachment:
                    attachments_in_memory.append(attachment)

            return attachments_in_memory
        except PermissionError as pe:
            raise PermissionError("Permissão negada para abrir o arquivo. Verifique se o arquivo está em uso.") from pe
        except OSError as ose:
            raise OSError(f"Ocorreu um erro ao tentar abrir o arquivo: {ose.strerror}") from ose
        except Exception as e:
            raise e

    
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


    def __init__(
        self, 
        data_user: DataUserController, 
        data_send: dict,
    ) -> None:
        
        super().__init__(
            data_user=data_user,
            data_send=data_send,
            list_columns=None
        )


    def read_emails(self) -> tuple[list[str], pd.DataFrame, list[str]]:
        if SenderEmailController.is_file_locked(self.data_send["spreadsheet_path"]):
            raise Exception("O arquivo de planilha está sendo utilizado por outro processo, feche-a e tente novamente.")
        
        df_emails: pd.DataFrame = pd.read_excel(self.data_send["spreadsheet_path"], converters={"STATUS": str})

        self.list_columns = df_emails.columns.tolist()
        variables_columns: list[str] = list(filter(
            lambda x: x not in ["E-mail", "STATUS", "PDF"], self.list_columns
        ))

        try:
            if not {"E-mail", "STATUS", "PDF"}.issubset(self.list_columns):
                raise KeyError("Coluna 'E-mail' ou 'STATUS' ou 'PDF' não encontrada na planilha.")
            
            df_no_duplicates: pd.DataFrame = df_emails.drop_duplicates(
                subset=self.list_columns, keep='first')

            df_no_duplicates.to_excel(self.data_send["spreadsheet_path"], index=False)
            
            colum_emails: list[str] = df_no_duplicates["E-mail"].tolist()

            return colum_emails, df_no_duplicates, variables_columns
        except Exception as error:
            raise Exception(f"Erro ao carregar emails: {error}")
        
    
    def verify_last_index_and_start_index(self, df_emails: pd.DataFrame) -> int:
        last_sent_index: int = df_emails[df_emails["STATUS"].isin(['ENVIADO', 'ERRO'])].index.max()
        return(last_sent_index + 1) if pd.notna(last_sent_index) else 0


    def get_values_of_spreadsheet(self, df_emails: pd.DataFrame, variables_columns: list[str], current_index: int) -> dict[str, str]:
        def has_value(value: str) -> str:
            return '' if value == 'nan' or value is None else value
        
        dynamic_values: dict[str, str] = {
            column: has_value(str(df_emails.loc[current_index, column]))
            for column in variables_columns
        }
        
        return dynamic_values


    def get_name_attachment(self, df_emails: pd.DataFrame, destination_email: str) -> list[str] | list:
        if destination_email in df_emails["E-mail"].values:
            attachments: str = df_emails.loc[df_emails["E-mail"] == destination_email, "PDF"].iloc[0]
            arquives_name_list: list[str] = []

            if pd.isna(attachments) or not attachments:
                return list()

            attachments = attachments.replace(' ', '')

            arquives_name_list.extend(attachments.split(';')) if ";" in attachments else arquives_name_list.append(attachments)

            return arquives_name_list
        return list()


    def update_message(self, columns_values: dict[str, str]) -> tuple[str, str, str]:
        message_copy: str = self.data_send["email_message"]
        title_copy: str = self.data_send["email_title"]
        
        for key, value in columns_values.items():
            message_copy = message_copy.replace(f"{{{key.lower()}}}", value)
            title_copy = title_copy.replace(f"{{{key.lower()}}}", value)
                
        link_whatsapp_copy: str = f"https://api.whatsapp.com/send?phone={self.data_send['whatsapp_redirect_number']}&text={self.data_send['redirect_message']}"

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


    def config_send_email(self, destination_email: str, copy_body_html: str, attachments: list[MIMEApplication] | None) -> None:
        server_smtp, port_smtp = self.type_verify_email()

        msg: MIMEMultipart = MIMEMultipart('alternative')
        msg['Subject'] = self.data_send["email_subject"]
        msg['From'] = self.data_user.email
        msg['To'] = destination_email
        msg.attach(MIMEText(copy_body_html, 'html', 'utf-8'))

        if attachments:
            for attachment in attachments:
                msg.attach(attachment)

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


    def write_on_console_and_txt(
        self, 
        destination_email: str, 
        destination_emails: list[str], 
        validator: bool, 
        current_index: int, 
        error: str = None,  
        interval_send_email: int = None,
    ) -> str:
        
        if not validator:
            message: str = (
                f"Erro ao enviar email para {destination_email} às {datetime.now().strftime('%d/%m/%Y-%H:%M:%S')}\n" 
                f"\nTotal de emails enviados: {current_index + 1} de {len(destination_emails)} Erro: {error}\n"
            )
            Log.write_error(self.data_user.email, message)
            return message

        message: str = (
            f"Email enviado para {destination_email} às {datetime.now().strftime('%d/%m/%Y-%H:%M:%S')}\nTotal de emails enviados: {current_index + 1} de {len(destination_emails)} "
            f"Intervalo de envio: {interval_send_email} segundos\n"
        )
        Log.write_success(self.data_user.email, message)
        return message
    
    
    def pre_process_emails(
        self, 
        df_emails: pd.DataFrame, 
        destination_email: str, 
        body_html_original: str, 
        variables_columns: list[str], 
        current_index: int
    ) -> list[str]:
        
        columns_values: dict[str, str] = self.get_values_of_spreadsheet(df_emails, variables_columns, current_index)
        message_copy, title_copy, link_whatsapp_copy = self.update_message(columns_values)
        attachments_list_in_memory: list[MIMEApplication] | None = SenderEmailController.load_attachments(
            self.get_name_attachment(df_emails, destination_email)
        )
        message_copy, title_copy, link_whatsapp_copy = self.update_message(columns_values)
        copy_body_html: str = self.replace_email_html(body_html_original, message_copy, title_copy, link_whatsapp_copy)
        self.config_send_email(destination_email, copy_body_html, attachments_list_in_memory)
        
    
    def error_env(
        self, 
        df_emails: pd.DataFrame, 
        destination_email: str, 
        destination_emails: list[str], 
        current_index: int, 
        error: Exception, 
        log_signal: pyqtBoundSignal
    ) -> None:
        
        df_emails.loc[current_index, "STATUS"] = 'ERRO'
        df_emails.to_excel(self.data_send["spreadsheet_path"], index=False)
        message_error: str = self.write_on_console_and_txt(destination_email, destination_emails, False, current_index, error)
        log_signal.emit(message_error)
        
    
    def process_email_sending(
        self, 
        df_emails: pd.DataFrame, 
        destination_email: str, 
        destination_emails: list[str], 
        current_index: int, 
        log_signal: pyqtBoundSignal,
        body_html_original: str,
        variables_columns: list[str]
    ) -> bool:
        
        random_interval: int = SenderEmailController.wait_random_send_email(self.data_send["send_interval"])
        
        try:
            self.pre_process_emails(df_emails, destination_email, body_html_original, variables_columns, current_index)
            df_emails.loc[current_index, "STATUS"] = 'ENVIADO'
            df_emails.to_excel(self.data_send["spreadsheet_path"], index=False)
            message_success: str = self.write_on_console_and_txt(destination_email, destination_emails, True, current_index, None, random_interval)
            log_signal.emit(message_success)
            time.sleep(random_interval)
        except SMTPAuthenticationError as sae:
            message_error: str = f"Erro de autenticação. Verifique o e-mail e senha do aplicativo., ou contate o suporte. {sae}"
            self.error_env(df_emails, destination_email, destination_emails, current_index, message_error, log_signal)
            return False
        except SMTPRecipientsRefused:
            message_error: str = f"O e-mail {destination_email} foi recusado pelo servidor SMTP. Tente iniciar os envios novamente ou feche o programa."
            self.error_env(df_emails, destination_email, destination_emails, current_index, message_error, log_signal)
            return True
        except (SMTPConnectError, SMTPServerDisconnected):
            message_error: str = "Conexão ou Falha com o servidor SMTP. Tente iniciar os envios novamente ou feche o programa."
            self.error_env(df_emails, destination_email, destination_emails, current_index, message_error, log_signal)
            return False
        except Exception as error:
            self.error_env(df_emails, destination_email, destination_emails, current_index, error, log_signal)
            return False
    

    def send_emails(self, log_signal: pyqtBoundSignal) -> None:
        body_html_original: str = SenderEmailController.load_html(self.data_send["html_path"])
        destination_emails, df_emails, variables_columns = self.read_emails()
        
        start_index: int = self.verify_last_index_and_start_index(df_emails)
        destination_emails = destination_emails[start_index:]
        
        if not destination_emails or start_index is None:
            raise Exception("Nenhum e-mail encontrado na planilha para envio. Cheque a coluna de E-mail ou STATUS.")

        for current_index, destination_email in enumerate(destination_emails):
            if (current_index + 1) > self.data_send["email_send_quantity"]:
                break
            
            flag_status: bool = self.process_email_sending(
                df_emails,
                destination_email,
                destination_emails,
                current_index,
                log_signal,
                body_html_original,
                variables_columns
            )
            
            if not flag_status:
                break