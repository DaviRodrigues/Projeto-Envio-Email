# Projeto Envio Email

Bem-vindo ao Projeto Envio Email! Este é um projeto de automação desenvolvido em Python para facilitar o envio de emails em massa.

## Índice

- [Introdução](#introdução)
- [Funcionalidades](#funcionalidades)
- [Tecnologias Utilizadas](#tecnologias-utilizadas)
- [Instalação](#instalação)
- [Fotos do Projeto](#fotos-do-projeto)
- [Como Usar](#como-usar)
- [Exemplo de Uso](#exemplo-de-uso)
- [Licença](#licença)

## Introdução

Este projeto foi criado para automatizar o envio de emails para múltiplos destinatários com a possibilidade de personalização de mensagens, inclusão de anexo e escolha de template html. Utiliza Python e bibliotecas específicas para gerenciar o envio de emails de maneira eficiente e segura.
Além disso, é aconselhável que para emails recém criados sejam enviados aos poucos para evitar banimentos e também limite de envios execido. Outro fator a se ressaltar é de que alguns domínios de email podem não estarem disponíveis o ideal é utilizar um do Google ou [webcertificados.com.br, webcertificado.com.br, outlook.com, hotmail.com, aol.com, icloud.com].

## Funcionalidades

- Envio de emails para uma lista de destinatários.
- Personalização do assunto e do corpo do email.
- Suporte para anexos.
- Registro de histórico de envio.

## Tecnologias Utilizadas

- **Python**: Linguagem de programação principal.
- **Biblioteca de Envio de Emails**: [smtplib](https://docs.python.org/3/library/smtplib.html).
- **Outras dependências**: Pandas, Email, Webbrowser, Json, Atexit, Random, Time, Os, Datetime, Pyqt5

## Instalação

1. Clone o repositório:
    ```bash
    git clone https://github.com/seu-usuario/projeto-envio-email.git
    cd projeto-envio-email
    ```

2. Crie e ative um ambiente virtual e utilize o requirements.txt (recomendado):
    ```bash
    python -m venv venv
    source .venv/bin/activate  # No Windows, use `.venv\Scripts\activate`
    ```

## Fotos do Projeto

- Tela de Login

![Tela de Login](https://github.com/DaviRodrigues/Projeto-Envio-Email/blob/main/img/Tela_Login_Email.png)

- Tela Principal

![Tela Principal](https://github.com/DaviRodrigues/Projeto-Envio-Email/blob/main/img/Tela_Principal_Email.png)

## Como Usar

   - Execute o script principal do projeto com interface:
     ```bash
     python Envio de emails com app.py
     ```
   -Ou execute o script principal do projeto sem interface:
     ```bash
     python Envio de emails sem app.py
     ```

   -Utilize a planilha base que se encontra em src/static para colocar os dados/emails;

   -Cadastre uma conta com senha de app do google no sistema e faça login;

   -Após isso, configure da melhor forma para envio, inicie e espere até começar os envios.

## Exemplo de Uso

Aqui está um exemplo básico de como usar este projeto para enviar um email:

```python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from config import EMAIL_ADDRESS, EMAIL_PASSWORD

def enviar_email(destinatario, assunto, corpo):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = destinatario
    msg['Subject'] = assunto

    msg.attach(MIMEText(corpo, 'plain'))

    with smtplib.SMTP('smtp.gmail.com', 587) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        print(f'Email enviado para {destinatario}')

# Exemplo de uso
destinatarios = ['exemplo1@dominio.com', 'exemplo2@dominio.com']
assunto = "Teste de Envio de Email"
corpo = "Este é um email de teste."

for destinatario in destinatarios:
    enviar_email(destinatario, assunto, corpo)
```

## Licença

Este projeto está licenciado sob a licença MIT. Veja o arquivo [LICENSE](link) para mais detalhes.

Agredeço por sua visita!
