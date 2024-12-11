import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import APIs

class SendEMail():
    def __init__(self) -> None:
        self.smtp_server = "smtp.gmail.com"
        self.port = 587
        self.sender_email = APIs.mail(email=True)
        self.sender_password = APIs.mail(password=True)
    
    def send(self, recEmail, subject, body):

        # Create a MIMEText object for the email body
        message = MIMEMultipart()
        message["From"] = self.sender_email
        message["To"] = recEmail
        message["Subject"] = subject

        # Add the body to the email
        message.attach(MIMEText(body, "plain"))

        try:
            # Set up the server connection with TLS encryption
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls(context=context)  # Start TLS encryption
                server.login(self.sender_email, self.sender_password)  # Log in to the email server
                server.sendmail(self.sender_email, recEmail, message.as_string())  # Send the email
                print("Email sent successfully!")
            return True
        except Exception as e:
            print(f"Error sending email: {e}")
            return False

if __name__=='__main__':
    # mail = SendEMail()
    # receiver_email = "hemanggour547@gmail.com"
    # subject = "Test Email"
    # body = "This is a test email sent from Python using Gmail."
    # mail.send(recEmail=receiver_email, subject=subject, body=body)
    pass