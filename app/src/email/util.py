from string import Template

def populateEmailSalutation(email_template, recipient_name):
    s = Template(email_template)
    data = dict(first_name=recipient_name)
    return s.safe_substitute(data)
