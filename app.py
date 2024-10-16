from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import pdfkit
import PyPDF2
from docx import Document
from PIL import Image
import pytesseract
import base64
from dotenv import load_dotenv
import os
import openai
from decision_engine import DecisionEngine,EscalateComplaintRule,AutoReplyRule,ForwardToBillingRule,Rule
from automation_module import execute_action
from multilingual_support import detect_language,translate_text
from advanced_sentiment import detect_emotions
from urgency_detection import detect_urgency
from anomaly_detection import is_anomalous,train_anomaly_detector
from intent_recognition import recognize_intent

SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

load_dotenv()

openai.api_key = os.getenv("OPENAI_API_KEY")

# Step 1: Obtain OAuth 2.0 credentials (from the JSON file)
flow = InstalledAppFlow.from_client_secrets_file(
    './credential.json', SCOPES)
creds = flow.run_local_server(port=3000)

# Step 2: Build Gmail service
service = build('gmail', 'v1', credentials=creds)
PDF_FOLDER="emails_pdf"
# Step 3: List the latest emails in the inbox
results = service.users().messages().list(userId='me', q='is:unread').execute()
messages = results.get('messages', [])

if not messages:
    print('No new messages found.')
else:
    for message in messages:
        msg = service.users().messages().get(userId='me', id=message['id']).execute()
        email_data = msg['snippet']
        print(f'Message snippet: {email_data}')

        # Convert the email to PDF
        email_html_content = f"<html><body><p>{email_data}</p></body></html>"
        output_pdf = f"email_{message['id']}.pdf"
        output_pdf_path = os.path.join(PDF_FOLDER, output_pdf)
        pdfkit.from_string(email_html_content, output_pdf_path)
        print(f"Email saved as PDF: {output_pdf}")

        detected_language = detect_language(email_data)
        print(f"Detected Language: {detected_language}")

        if detected_language != 'English':
            translated_content = translate_text(email_data)
        else:
            translated_content = email_data


        # Step 4: Detect language using OpenAI
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Detect the language of the following text:"},
                {"role": "user", "content": email_data}
            ]
        )
        language = response['choices'][0]['message']['content']
        print(f"language: {language}")


        summary_prompt = f"Summarize the following email:\n\n{email_data}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": summary_prompt}]
        )
        summary = response['choices'][0]['message']['content']
        print(f"summary: {summary}")

        sentiment_prompt = f"Analyze the sentiment (positive, negative, neutral) of the following email:\n\n{email_data}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": sentiment_prompt}]
        )
        sentiment = response['choices'][0]['message']['content']
        print(f"sentiment: {sentiment}")

        subject_prompt = f"Analyze the subject of the following email shortly:\n\n{email_data}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": subject_prompt}]
        )
        subject = response['choices'][0]['message']['content']
        print(f"subject: {subject}")

        classification_prompt = f"Classify the following email into one of the categories: Billing, Technical Support, General Inquiry, Complaint.\n\n{email_data}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": classification_prompt}]
        )
        classification = response['choices'][0]['message']['content']
        print(f"classification: {classification}")

        name_prompt = f"Classify the sender name in the email \n\n{email_data}"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": name_prompt}]
        )
        name = response['choices'][0]['message']['content']
        print(f"sender name: {name}")

        rules = [
            AutoReplyRule(),
            ForwardToBillingRule(),
            EscalateComplaintRule(),
        ]
        engine = DecisionEngine(rules)
        email_data = {
            'from': 'triagetesting123@gmail.com',
            'subject':subject,
            'classification': classification, 
            'sentiment': sentiment,
            'language': language,
            'content': summary
        }
        action = engine.decide(email_data)
        print(f"Next action: {action}")
        is_urgent = detect_urgency(summary)
        print(f"Is Urgent: {is_urgent}\n\n")
        emotions = detect_emotions(summary)
        print(f"Detected Emotions: {emotions}\n\n")
        normal_emails = ['Thank you for your help.', 'Can you provide an update on my order?']
        model = train_anomaly_detector(normal_emails)

        anomaly = is_anomalous(summary, model)
        print(f"Anomalous Email: {anomaly}") 

        intent = recognize_intent(summary)
        print(f"Recognized Intent: {intent}")

    
        res=execute_action(action, email_data,name)
        print("outcome: ",res)
        # Step 5: Extract attachments and process them (if available)
        if 'parts' in msg['payload']:
            for part in msg['payload']['parts']:
                if part['filename']:
                    attachment_id = part['body']['attachmentId']
                    attachment = service.users().messages().attachments().get(userId='me', messageId=message['id'], id=attachment_id).execute()
                    file_data = base64.urlsafe_b64decode(attachment['data'])
                    
                    path = part['filename']
                    with open(path, 'wb') as f:
                        f.write(file_data)
                    print(f"Attachment saved: {path}")
