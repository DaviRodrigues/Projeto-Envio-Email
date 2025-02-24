from dataclasses import dataclass

@dataclass
class EmailDataSenderSchema:
    spreadsheet_path: str
    html_path: str
    email_send_quantity: int
    send_interval: int
    email_subject: str
    email_title: str
    email_message: str
    whatsapp_redirect_number: str
    redirect_message: str

