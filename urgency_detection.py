def detect_urgency(email_content):
    urgent_keywords = ['urgent', 'immediately', 'asap', 'as soon as possible', 'critical']
    urgency_score = 0
    for keyword in urgent_keywords:
        if keyword in email_content.lower():
            urgency_score += 1
    return urgency_score > 0

# Example usage
# email_content = "This is a critical issue that needs to be resolved immediately!"
