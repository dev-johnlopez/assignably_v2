import smtplib
from app.src.util.html import strip_tags
from threading import Thread
from flask import current_app
from flask_mail import Message
from app import mail
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template
from app.src.util.html import strip_tags

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_sample_email(user, recipient_name, subject, template):
    html_body = popuplateContactName(template, recipient_name)
    text_body = strip_tags(html_body)
    # set up the SMTP server
    s = smtplib.SMTP(host=user.user_contact.marketing_email_host, port=user.user_contact.marketing_email_port)
    s.starttls()
    s.login(user.user_contact.marketing_email, user.user_contact.marketing_email_password)
    send_email(subject, user.user_contact.marketing_email, [user.email], text_body, html_body, smtp=s)
    # Terminate the SMTP session and close the connection
    s.quit()

def send_email(subject, sender, recipients, text_body, html_body,
               attachments=None, sync=False, smtp=None):

    # setup the parameters of the message
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    msg.html = html_body
    if attachments:
        for attachment in attachments:
            msg.attach(*attachment)

    #msg = MIMEMultipart('alternative')
    #msg['From']=sender.email
    #msg['To']=recipient.email
    #msg['Subject']=subject
    #part1 = MIMEText(text_body, 'plain')
    #part2 = MIMEText(html_body, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    #msg.attach(part1)
    #msg.attach(part2)

    if smtp is not None:
        #send the message via the SMTP server set up earlier.
        smtp.sendmail(sender, [recipients], msg.as_string())
    elif sync:
        mail.send(msg)
    else:
        Thread(target=send_async_email,
            args=(current_app._get_current_object(), msg)).start()
    del msg

def popuplateContactName(email_template, recipient_name):
    s = Template(email_template)
    data = dict(first_name=recipient_name)
    return s.safe_substitute(data)
