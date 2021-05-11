import os
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from sendgrid import SendGridAPIClient

def sendgridmail(user,TEXTT,TEXT):
    sg = SendGridAPIClient('Please use your sendgrid api key')
    from_email = Email("lokesh12215@gmail.com")  # Change to your verified sender
    to_email = To(user)  # Change to your recipient
    subject = "Digital Payment Book"
    content = Content("text/plain",TEXT)
    mail = Mail(from_email, to_email, subject, content)
    response = sg.send(mail)
    print(response.status_code)
    print(response.body)
    print(response.headers)
    from_email = Email("lokesh12215@gmail.com")  # Change to your verified sender
    to_email = To("lokesh12215@gmail.com")  # Change to your recipient
    subject = "Digital Payment Book"
    content = Content("text/plain",TEXTT)
    mail = Mail(from_email, to_email, subject, content)
    response = sg.send(mail)
    print(response.status_code)
    print(response.body)
    print(response.headers)
   

