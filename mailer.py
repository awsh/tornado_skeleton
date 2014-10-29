import tornado.template
import config
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Really need to fix all of the email handling


def send(to, template, data):
    '''
    send an email

    subject is loaded from a dictionary depending based off of
    the template used

    the email template path is set in config

    two templates are loaded. an html and a txt

    '''

    subject = {"account_activation": "Blah Blah Account Activation"}

    loader = tornado.template.Loader(config.EMAIL_TEMPLATE_PATH)
    html = loader.load(
        "{0}.html".format(template)).generate(data=data).decode("utf-8")
    text = loader.load(
        "{0}.txt".format(template)).generate(data=data).decode("utf-8")

    msg = MIMEMultipart('alternative')
    msg['Subject'] = subject[template]
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
    send("admin@awsh.org", "account_activation", {"activation_id": "123454"})
