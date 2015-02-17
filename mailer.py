import tornado.template
import config
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Really need to fix all of the email handling

def send(to, subject, template, **kwargs):

    loader = tornado.template.Loader(config.EMAIL_TEMPLATE_PATH)
    html = loader.load(
        "{0}.html".format(template)).generate(data=kwargs).decode("utf-8")
    text = loader.load(
        "{0}.txt".format(template)).generate(data=kwargs).decode("utf-8")

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject
    msg['From'] = "{0} <{1}>".format(config.EMAIL_FROM_NAME,
                                     config.EMAIL_FROM_ADDRESS)
    msg['To'] = to

    part1 = MIMEText(text, 'plain')
    part2 = MIMEText(html, 'html')

    msg.attach(part1)
    msg.attach(part2)

    with smtplib.SMTP(config.EMAIL_HOST, config.EMAIL_PORT) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.ehlo()
        smtp.login(config.EMAIL_USER, config.EMAIL_PASSWORD)
        smtp.sendmail(msg['From'], msg['To'], msg.as_string())

if __name__ == "__main__":
    send("ashiflett@lowtempind.com", "forgot password", "password_reset", reset_key="123454", requested_ip='127.0.0.1')
