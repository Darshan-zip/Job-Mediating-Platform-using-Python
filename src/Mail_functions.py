import smtplib
import random
def send_otp(s):
    server=smtplib.SMTP('smtp.gmail.com')
    server.ehlo()
    server.starttls()
    server.ehlo
    with open('password.txt','r') as x:
        password=x.read()
    
    server.login('darshansarathy23@gmail.com',password)
    subject="Job - Mediating - Platform OTP"
    body="Forgot Password?\nUse this OTP to change the Password\n\t"
    otp=random.randrange(1000,9999)
    body=body+str(otp)
    msg=f"subject:{subject}\n\n\n{body}"
    
    server.sendmail(
        "darshansarathy23@gmail.com",
        s,
        msg
    )
    print("OTP sent successfully!")
    return otp

def Hire_email_r2j(J,R):
    server=smtplib.SMTP('smtp.gmail.com')
    server.ehlo()
    server.starttls()
    server.ehlo
    with open('password.txt','r') as x:
        password=x.read()
    
    server.login('darshansarathy23@gmail.com',password)
    subject="Job - Mediating - Platform Job Offer"
    body="Hey "+J[0]+"!.We have come across alot of profiles on the Job meditiating platform but after indefinite number of hours of analysis, our team has come to the conclusion that you meet all the requirements for the ROLE:"+R[8]+". \nWe hope to have a formal conversion with you to discuss your salary and other specifications at our office. All the Best!\n"
    x="Office address:"+R[2]+"\nFor further Details, visit my profile on the Job-Mediating platform.\nUsername:"+R[22]

    sign="\nWith Best Regards,\n"+R[0]+"\n"+R[3]+"\n"+R[11]

    body=body+x+sign
    msg=f"subject:{subject}\n\n\n{body}"
    print(J[5])
    #sending mail thru admin for security reasons
    server.sendmail(
        "darshansarathy23@gmail.com",
        J[5],
        msg
    )
    return(1)
    
def Apply_email_j2r(J,R):
    server=smtplib.SMTP('smtp.gmail.com')
    server.ehlo()
    server.starttls()
    server.ehlo
    with open('password.txt','r') as x:
        password=x.read()
    
    server.login('darshansarathy23@gmail.com',password)
    subject="Job - Mediating - Platform Application"
    body="Hello "+R[0]+".I came across your company in the Job-Mediating Platform.I went through all your company details and its requirements and I feel I am suitable for this job. It would really help me if you could search up my username on the Job-Mediating Platform and have a look at my resume as it would tell you more about me.\nUsername:"+J[18]
    x="\n"

    sign="\nI hope for a quick response from your side.\nWith Best Regards,\n"+J[0]

    body=body+x+sign
    msg=f"subject:{subject}\n\n\n{body}"
    print(R[7])
    server.sendmail(
        "darshansarathy23@gmail.com",
        R[7],
        msg
    )
    print("Hire mail sent successfully!")
    return (1)

if __name__=="__main__":
    send_otp()