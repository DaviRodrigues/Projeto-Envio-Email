from src.schemas.EmailDataSenderSchema import EmailDataSenderSchema

# aqui você gera as dataclasses com os dados para serem enviados
email_data_list = [
    EmailDataSenderSchema(
        spreadsheet_path="C:\Projects\Disparador Email Agendador de Tarefas\src\static\Enviar e-mails.xlsx",
        html_path="C:\Projects\Disparador Email Agendador de Tarefas\src\static\index.html",
        email_send_quantity=2,
        send_interval=10,
        email_subject="Promoção Especial",
        email_title=" ",
        email_message=" ",
        whatsapp_redirect_number="553284598541",
        redirect_message="Olá, desejo saber mais"
    ),
        EmailDataSenderSchema(
        spreadsheet_path="C:\Projects\Disparador Email Agendador de Tarefas\src\static\Enviar e-mails 2.xlsx",
        html_path="C:\Projects\Disparador Email Agendador de Tarefas\src\static\index 2.html",
        email_send_quantity=2,
        send_interval=10,
        email_subject="Promoção Especial",
        email_title=" ",
        email_message=" ",
        whatsapp_redirect_number="553284598541",
        redirect_message="Olá, desejo saber mais"
    ),
]

