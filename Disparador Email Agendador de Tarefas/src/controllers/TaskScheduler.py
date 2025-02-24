from src.controllers.EmailSender import EmailSender
from src.schemas.EmailDataSenderSchema import EmailDataSenderSchema
from src.schemas.LoginSchema import LoginSchema
from src.data.EmailsSenderData import email_data_list
from src.data.LoginsData import login_data_list
import schedule
import time
import threading

def init_task():
    horario: str = "13:09"
    print(f"Iniciando Agendador de Envio do Emails. Aguarde até horário de {horario}...")
    schedule.every().day.at(horario).do(email_run_threading)

    while True:
        schedule.run_pending()
        time.sleep(1)

def init_email_sender(email_data: EmailDataSenderSchema, login_data: LoginSchema):
    email_sender: EmailSender = EmailSender(email_data.__dict__, login_data)
    email_sender.requisicao_iniciar_envios()

def email_run_threading():
    threads = list()

    for email_data, login_data  in zip(email_data_list, login_data_list):

        thread = threading.Thread(target=init_email_sender, args=(email_data, login_data))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()