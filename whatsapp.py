import requests

# Replace with your values
APP_ID = '123'
APP_SECRET = 'xxx'
LONG_LIVED_TOKEN = 'xxx'
PHONE_NUMBER_ID = 'xxxx'
RECIPIENTS_FILE = 'recipients.txt'

def refresh_token():
    url = f"https://graph.facebook.com/v22.0/oauth/access_token"
    params = {
        "grant_type": "fb_exchange_token",
        "client_id": APP_ID,
        "client_secret": APP_SECRET,
        "fb_exchange_token": LONG_LIVED_TOKEN
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()["access_token"]

def get_recipient_phones_and_names(filename):
    recipients = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line:
                # Expecting format: phone,name
                parts = line.split(',', 1)
                if len(parts) == 2:
                    phone, name = parts[0].strip(), parts[1].strip()
                    recipients.append((phone, name))
    return recipients

def send_membership_due_message(access_token, recipient_phone, name):
    url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": recipient_phone,
        "type": "template",
        "template": {
            "name": "ststephens_membership_autopay",
            "language": {"code": "en_US"},
            "components": [
                {
                    "type": "header",
                    "parameters": [
                        {
                            "type": "image",
                            "image": {
                                "link": "https://ststephenssanjose.org/images/logo/logo1.png"
                            }
                        }
                    ]
                },
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": name}
                    ]
                }
            ]
        }
    }
    response = requests.post(url, headers=headers, json=data)
    print(f"Membership message to {recipient_phone} ({name}): {response.status_code} {response.text}")

def send_food_signup_reminder(access_token, recipient_phone, name):
    url = f"https://graph.facebook.com/v22.0/{PHONE_NUMBER_ID}/messages"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    data = {
        "messaging_product": "whatsapp",
        "to": recipient_phone,
        "type": "template",
        "template": {
            "name": "ststephens_food_sponsor_signup_reminder",
            "language": {"code": "en_US"},
            "components": [
                {
                    "type": "header",
                    "parameters": [
                        {
                            "type": "image",
                            "image": {
                                "link": "https://ststephenssanjose.org/images/logo/logo1.png"
                            }
                        }
                    ]
                },
                {
                    "type": "body",
                    "parameters": [
                        {"type": "text", "text": name}
                    ]
                }
            ]
        }
    }
    response = requests.post(url, headers=headers, json=data)
    print(f"Food signup reminder to {recipient_phone} ({name}): {response.status_code} {response.text}")

if __name__ == "__main__":
    token = refresh_token()
    recipients = get_recipient_phones_and_names(RECIPIENTS_FILE)
    for phone, name in recipients:
        send_membership_due_message(token, phone, name)
        send_food_signup_reminder(token, phone, name)
        