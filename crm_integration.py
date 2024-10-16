import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve credentials from environment variables
consumer_key = os.getenv('SALESFORCE_CONSUMER_KEY')
consumer_secret = os.getenv('SALESFORCE_CONSUMER_SECRET')
username = os.getenv('SALESFORCE_USERNAME')
password = os.getenv('SALESFORCE_PASSWORD')
security_token = os.getenv('SALESFORCE_SECURITY_TOKEN')

# Ensure the password includes the security token
password_with_token = f"{password}{security_token}"

# Log the credentials (remove this in production)
print("Consumer Key:", consumer_key)
print("Consumer Secret:", consumer_secret)
print("Username:", username)
print("Password with Token:", password_with_token)

# Use the correct token URL based on your Salesforce environment
token_url = "https://login.salesforce.com/services/oauth2/token" 

# Parameters for the token request
data = {
    'grant_type': 'password',
    'client_id': consumer_key,
    'client_secret': consumer_secret,
    'username': username,
    'password': password
}

# Make the POST request to get the access token
response = requests.post(token_url, data=data)

# Check the response
if response.status_code == 200:
    access_token = response.json().get('access_token')
    instance_url = response.json().get('instance_url')
    print(f"Access token: {access_token}")
    print(f"Instance URL: {instance_url}")
else:
    print(f"Failed to get access token. Status code: {response.status_code}")
    print(response.text)

# Example function to use the access token
def get_salesforce_contact(contact_id, access_token, instance_url):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    data = {
    'sentiment__c': 'positive',
    'MobilePhone':9025105082,
    'Description':'this is for triage crm testing'
    }
    print("email_data: ",data)
    response = requests.patch(f'{instance_url}/services/data/v52.0/sobjects/Contact/{contact_id}', 
                              headers=headers, json=data)
    response = requests.get(f'{instance_url}/services/data/v52.0/sobjects/Contact/{contact_id}', 
                              headers=headers, json=data)
    
    if response.status_code == 200:
        print("fetched successfully")
        return response.json()
    elif response.status_code == 204: 
        print("Contact updated successfully.")
    else:
        print(f"Failed to fetch contact: {response.status_code}")
        print(response.text)




def get_contact_by_email(email, instance_url, access_token):
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    # SOQL query to search for contact by email
    query = f"SELECT Id, FirstName, LastName, Email FROM Contact WHERE Email = '{email}'"
    url = f"{instance_url}/services/data/v52.0/query?q={query}"
    
    # Make the GET request to Salesforce Query API
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        result = response.json()
        if result['totalSize'] > 0:
            contact = result['records'][0]
            contact_id = contact['Id']
            print(f"Contact ID: {contact_id}")
            return contact_id
        else:
            print("No contact found with this email.")
            return None
    else:
        print(f"Failed to query contact: {response.status_code}")
        print(response.text)
        return None
    


email = 'iamnithish100@gmail.com'
contact_id = get_contact_by_email(email, instance_url, access_token)
# Use the access token to fetch a contact record


contact_data = get_salesforce_contact(contact_id, access_token, instance_url)
print(contact_data)

