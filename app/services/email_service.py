
import os
import smtplib
import ssl

from email.message import EmailMessage


def enviar_email(
    destinatario: str,
    asunto: str,
    contenido: str,
    archivos: list
):
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")

    if not smtp_user or not smtp_password:
        raise ValueError(
            "No está configurada la cuenta Gmail en el servidor."
        )

    mensaje = EmailMessage()

    mensaje["Subject"] = asunto
    mensaje["From"] = smtp_user
    mensaje["To"] = destinatario

    mensaje.set_content(contenido)

    for nombre, datos, subtipo in archivos:
        mensaje.add_attachment(
            datos,
            maintype="application",
            subtype=subtipo,
            filename=nombre
        )

    contexto = ssl.create_default_context()

    with smtplib.SMTP(
        smtp_host,
        smtp_port,
        timeout=30
    ) as servidor:

        servidor.ehlo()
        servidor.starttls(context=contexto)
        servidor.ehlo()

        servidor.login(smtp_user, smtp_password)
        servidor.send_message(mensaje)

    return True
