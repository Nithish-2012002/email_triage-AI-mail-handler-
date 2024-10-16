import smtplib
from email.message import EmailMessage
import pymysql
from response_generation import generate_response

def send_email(to_address, subject, body, attachments=None):
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = 'triagetesting123@gmail.com'  # Replace with your email
    msg['To'] = to_address
    msg.set_content(body)

    # Attach files if any
    if attachments:
        for file_path in attachments:
            with open(file_path, 'rb') as f:
                file_data = f.read()
                file_name = f.name
            msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    # Send the email via SMTP server
    with smtplib.SMTP('smtp.gmail.com', 587) as server:  # Replace with your SMTP server and port
        server.starttls()
        server.login('triagetesting123@gmail.com', 'pept ypso brul rrvv')  # Use environment variables or a secure method
        server.send_message(msg)
        print("Email sent successfully.")

def forward_email(original_email_data, forward_to_address):
    # Prepare a forward message body
    forward_subject = "Fwd: " + original_email_data['subject']
    forward_body = f"Forwarded message:\n\nFrom: {original_email_data['from']}\n\n{original_email_data['content']}"
    
    # Use the send_email function to forward the message
    send_email(
        to_address=forward_to_address,
        subject=forward_subject,
        body=forward_body
    )
def escalate_to_manager(email_data,name):
    reply = generate_response(email_data, name)
    print(f"Generated Reply:\n\n{reply}")

def escalate_to_human(email_data):
    conn = pymysql.connect(
        host='localhost',  
        user='root',       
        password='',      
        db='emails'
    )
    try:
        with conn.cursor() as c:
            c.execute('''
                INSERT INTO emails (sender, subject, content, classification, sentiment, action)
                VALUES (%s, %s, %s, %s, %s, %s)
            ''', (
                email_data['from'],
                email_data['subject'],
                email_data['content'],
                email_data['classification'],
                email_data['sentiment'],
                'escalate_to_human'
            ))
        conn.commit()
    finally:
        conn.close()
        print("Email escalated to human agent.")

# Example usage
def execute_action(action, email_data, name):
    if action == 'auto_reply':
        send_email(
            to_address=email_data['from'],
            subject="Re: " + email_data['subject'],
            body="Thank you for reaching out. We have received your inquiry."
        )
    elif action == 'forward_to_billing':
        forward_email(email_data, 'iamnithish100@gmail.com')
    elif action == 'escalate_to_human':
        escalate_to_human(email_data)
    elif action == 'escalate_to_manager':
        escalate_to_manager(email_data, name)
    else:
        print("No action taken.")

# Sample email_data


# Assume action was determined earlier
