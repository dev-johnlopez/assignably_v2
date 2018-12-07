from collections import OrderedDict
import json

def generateOutlookMessage(subject,  content, recipient_email_addresses, content_type=1, attachments=[], save_to_sent_items=False):
    data = OrderedDict()
    data['message'] = {}
    data['message']['subject'] = subject
    data['message']['importance'] = 'Normal'
    data['message']['body'] = {}
    data['message']['body']['contentType'] = "HTML"
    data['message']['body']['content'] = content
    data['message']['toRecipients'] = []
    for recipient in recipient_email_addresses:
        emailData = {}
        emailData['emailAddress'] = {}
        emailData['emailAddress']['address'] = recipient
        data['message']['toRecipients'].append(emailData)
    return data
    #data['Message']['Subject'] = subject
    #data['Message']['Body'] = {}
    #data['Message']['Body']['ContentType'] = str(content_type)
    #data['Message']['Body']['Content'] = "test"
    #data['Message']['ToRecipients'] = []
    #for recipient in recipient_email_addresses:
    #    emailData = {}
    #    emailData['EmailAddress'] = {}
    #    emailData['EmailAddress']['Address'] = recipient
    #    data['Message']['ToRecipients'].append(emailData)
    #if len(attachments) > 0:
    #    data['Message']['Attachements'] = []
    #    #TODO validate attachments
    #    for attachment in attachments:
    #        attachmentData = {}
    #        attachmentData['@odata.type'] = "#Microsoft.OutlookServices.FileAttachment"
    #        attachmentData['Name'] = attachment['Name']
    #        attachmentData['ContentBytes'] = attachment['ContentBytes']
    #        data['Message']['Attachements'].append(attachmentData)
    #data['saveToSentItems'] = "false"
    #return json.dumps(data)


#
#    "subject":"Did you see last night's game?",
#    "importance":"Low",
#    "body":{
#        "contentType":"HTML",
#        "content":"They were <b>awesome</b>!"
#    },
#    "toRecipients":[
#        {
#            "emailAddress":{
#                "address":"AdeleV@contoso.onmicrosoft.com"
#            }
#        }
#    ]
#}

    {
        "message": {"body": {"content": "test", "contentType": "HTML"}, "subject": "test", "toRecipients": [{"emailAddress": {"address": "john@johnlopez.org"}}], "importance": "Low"}}


#{
#  "Message": {
#    "Subject": "Meet for lunch?",
#    "Body": {
#      "ContentType": "Text",
#      "Content": "The new cafeteria is open."
#    },
#    "ToRecipients": [
#      {
#        "EmailAddress": {
#          "Address": "garthf@a830edad9050849NDA1.onmicrosoft.com"
#        }
#      }
#    ],
#    "Attachments": [
#      {
#        "@odata.type": "#Microsoft.OutlookServices.FileAttachment",
#        "Name": "menu.txt",
#        "ContentBytes": "bWFjIGFuZCBjaGVlc2UgdG9kYXk="
#      }
#    ]
#  },
#  "SaveToSentItems": "false"
#}



#{
#    "SaveToSentItems": "false",
#    "Message": {
#        "Attachements": [],
#        "Subject": "Meet for Lunch?",
#        "Body": {
#            "ContentType": 1,
#            "Content": "The new cafeteria is open."
#        },
#        "ToRecipients": [
#            {
#                "EmailAddress": {
#                    "Address": "johnny.lopez617@gmail.com"
#                }
#            }
#        ]
#    }
#}
