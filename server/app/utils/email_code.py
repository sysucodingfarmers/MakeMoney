import smtplib
from email.mime.text import MIMEText
from email.header import Header

def send_email_code(email_code, target_email):
  # 第三方SMTP服务
  mail_host = 'smtp.163.com'
  mail_user = 'sysu_makemoney'
  mail_pass = 'sysu2019'

  subject = '【挣闲钱】验证码：' + email_code

  sender = 'sysu_makemoney@163.com'
  receiver = target_email

  mail_msg = "欢迎注册挣闲钱\n你的验证码是："
  mail_msg += email_code
  message = MIMEText(mail_msg, 'plain', 'utf-8')
  message['Subject'] = Header(subject, 'utf-8')
  message['From'] = sender
  message['To'] = receiver

  try:
    smtpObj = smtplib.SMTP()
    print("连接中")
    smtpObj.connect(mail_host, 25)
    print("连接成功")
    smtpObj.login(mail_user, mail_pass)
    print("登录成功")
    smtpObj.sendmail(sender, receiver, message.as_string())
    print("发送成功")
    return True
  except smtplib.SMTPException:
    print("Error: 无法发送邮件")
    return False