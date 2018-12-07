from flask import flash
import smtplib
from app.src.util.html import strip_tags
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from string import Template



def send_mail(sender, recipient, subject, html_msg):
    # set up the SMTP server
    s = smtplib.SMTP(host=sender.user_contact.marketing_email_host, port=sender.user_contact.marketing_email_port)
    s.starttls()
    s.login(sender.user_contact.marketing_email, sender.user_contact.marketing_email_password)

    # setup the parameters of the message
    msg = MIMEMultipart('alternative')
    msg['From']=sender.email
    msg['To']=recipient.email
    msg['Subject']=subject

    text_msg = strip_tags(html_msg)
    #Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText(text_msg, 'plain')
    part2 = MIMEText(html_msg, 'html')

    # Attach parts into message container.
    # According to RFC 2046, the last part of a multipart message, in this case
    # the HTML message, is best and preferred.
    msg.attach(part1)
    msg.attach(part2)

    # send the message via the server set up earlier.
    s.sendmail(sender.email, recipient, msg.as_string())
    del msg

    # Terminate the SMTP session and close the connection
    s.quit()

def flashFormErrors(form):
    for field, errors in form.errors.items():
        for error in errors:
            flash('{}: {}'.format(getattr(form, field).label.text, error), 'error')


def getEmailTemplate(deal):
    return '<p>Hello $first_name!</p>\
    <p><b>REPLACE THIS TEXT</b></p>\
    <p>Fernando Angelucci<br />\
    Senior Managing Partner<br />\
    Titan Wealth Group<br />\
    Urban RE<br />\
    (630) 408-8090<br />\
    3023 N. Clark St., #140<br />\
    Chicago, IL 60657</p>\
    <p>NOTICE:  If you would like to stop receiving emails from this sender, please respond \"Unsubscribe\". This e-mail message and any attachments or links are confidential and may be privileged. E-mails sent or received shall neither constitute acceptance of conducting transactions via electronic means nor create a binding contract in the absence of a fully signed written agreement. This information may not be reproduced or redistributed in whole or in part. \
    This communication does not constitute an offer, solicitation or recommendation to sell or an offer to purchase any securities, investment products or investment advisory services. The information contained in this communication is not intended to provide, and should not be relied on upon for, accounting, legal, or tax advice. By sending this e-mail, the sender does not consent to conduct any transactions that may be the subject of this email by \
    electronic means. Any statements made are for informational purposes only; they are deemed to be reasonable approximations based on information available today, but no guarantee or assurance can be provided as to their accuracy, and they may not offer a comprehensive representation. It is the recipient\'s responsibility to do their own due diligence and verify all information. Opinions of value / rents are given as a courtesy and no guarantees are \
    expressed or implied. Any assignments of contractual rights to purchase property are assigned for cash or hard money. Any assignment of contracts are subject to errors, omissions, deletions, additions, and cancellations. Any assignments of contractual rights to purchase property are assigned "as is" and "where is" with absolutely no warranties written or oral.</p>'

def popuplateEmailTemplateForContact(email_template, contact):
    s = Template(email_template)
    data = dict(first_name=contact.first_name)
    return s.safe_substitute(data)
