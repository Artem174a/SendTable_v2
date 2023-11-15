import smtplib
from enum import IntEnum
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email_validator import validate_email, EmailNotValidError


class SmtpPorts(IntEnum):
    PORT_587 = 587
    PORT_465 = 465


class Validation:
    @staticmethod
    def validate_email_address(email: str) -> bool:
        """
        Проверяет валидность email-адреса.

        :param email: Строка с email-адресом для проверки.
        :return: True, если адрес валиден, в противном случае False.
        """
        try:
            validate_email(email)
            return True
        except EmailNotValidError:
            return False

    @staticmethod
    def validate_email_list(emails: list) -> list:
        """
        Проверяет валидность списка email-адресов.

        :param emails: Список email-адресов для проверки.
        :return: Список валидных email-адресов.
        """
        return [email for email in emails if Validation.validate_email_address(email)]


class Mailing(smtplib.SMTP_SSL):
    def __init__(
            self,
            sender_email: str,
            sender_password: str,
            port: int = SmtpPorts.PORT_587
    ):
        super().__init__()
        if not Validation.validate_email_address(sender_email):
            raise ValueError("Invalid sender email address")

        self.sender_email = sender_email
        self.sender_password = sender_password
        self.port = port

        self.host: str = "smtp." + self.sender_email.split('@')[1]

        try:
            print(f'Авторизация ...')
            self.smtpObj = smtplib.SMTP(str(self.host), int(self.port))
            self.smtpObj.ehlo()
            self.smtpObj.starttls()
            self.smtpObj.login(self.sender_email, self.sender_password)
        except Exception as e:
            print(f'Failed to connect to SMTP\nError: {e}')
            raise e
        else:
            print(f'Авторизован!')

    def run_mailing(self, subject: str, body: str, recipients: list, file_path: str = None, html_message: str = None):
        """
        :param subject: Тема письма.
        :param body: Тело письма.
        :param recipients: Список адресов получателей.
        :param file_path: Путь к файлу для прикрепления.
        :param html_message: HTML-сообщение.
        """
        try:
            validated_recipients = Validation.validate_email_list(recipients)

            for recipient in validated_recipients:
                message = MIMEMultipart()
                message['Subject'] = subject
                message['From'] = self.sender_email
                message['To'] = recipient

                if body:
                    message.attach(MIMEText(body, 'plain'))

                if file_path:
                    with open(file_path, "rb") as attachment:
                        part = MIMEApplication(attachment.read(), Name="attachment")
                        part['Content-Disposition'] = f'attachment; filename="{file_path}"'
                        message.attach(part)

                if html_message:
                    html_part = MIMEText(html_message, 'html')
                    message.attach(html_part)

                self.smtpObj.sendmail(self.sender_email, recipient, message.as_string())
                print(f"Письмо отправлено: \nПолучатель - {recipient}")
        except Exception as e:
            print(f"Error sending email: {e}")
        finally:
            self.smtpObj.quit()
