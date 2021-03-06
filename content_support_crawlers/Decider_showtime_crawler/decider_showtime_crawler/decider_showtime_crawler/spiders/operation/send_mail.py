import smtplib,ssl
import sys
import os
import socket
import ntpath
import csv
import datetime
from email.mime.base import MIMEBase 
from email import encoders
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

class send_emails:

    def __init__(self):
        self.sender_email=''
        self.receiver_email=''
        self.password=''

    def user_input(self):
        self.sender_email="jyoshna@headrun.com"
        self.receiver_email=["hott@headrun.com"]
        self.password="9542935822"

    def user_message(self):
        text="""Hi Team,

    Showtime titles from Decider for the month of %s.
        
    Please find the attachment.

    

    Thanks,
    Jyoshna, """%datetime.datetime.now().strftime('%B')
    
        return text  

    def read_attachment(self,attachment_):
        with open(attachment_, "rb") as attachment:
            # Add file as application/octet-stream
            # Email client can usually download this automatically as attachment
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())
            # Encode file in ASCII characters to send by email    
            encoders.encode_base64(part)
            # Add header as key/value pair to attachment part
            part.add_header(
                "Content-Disposition",
                "attachment", filename=ntpath.basename(attachment_)) 
            return part     

    def main(self):
        self.user_input()
        message=MIMEMultipart("alternative")
        message["Subject"]="Decider Showtime Result on %s"%(datetime.datetime.now().strftime('%b %d, %Y'))
        message["From"]=self.sender_email
        message["To"]=",".join([email_id for email_id in self.receiver_email])
        port =587
        text=self.user_message()
        part1=MIMEText(text,"plain")
        message.attach(part1)
        filenames=['showtime_added_content_%s.csv'%(datetime.datetime.now().strftime('%b %d, %Y'))]
        for file in filenames:
            with open(os.getcwd()+'/operation/attachments/'+file, 'r') as csvfile:
                csv_dict = [row for row in csv.DictReader(csvfile)]
                print("the data count:",len(csv_dict))
                if len(csv_dict) > 1:
                    attachment=os.getcwd()+'/operation/attachments/'+file
                    file_=self.read_attachment(attachment)
                    message.attach(file_)
                    try:
                        server = smtplib.SMTP("smtp.gmail.com",port)
                        server.ehlo()
                        server.starttls()
                        server.login(self.sender_email,self.password)
                        server.sendmail(self.sender_email,self.receiver_email,message.as_string())
                        server.quit()
                        print("mail sent to %s %s"%(",".join(self.receiver_email),datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
                    except socket.error as e:
                        print("retrying........",type(e))
                        self.main()
                else:
                    print('csv file is empty........%s'%(datetime.datetime.now().strftime('%b %d, %Y')))        

