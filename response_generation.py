import openai

def generate_response(email_content, customer_name, previous_interactions="none"):
    prompt = f"""
    You are a customer service assistant. Write a professional and empathetic email response to the customer.

    Customer Name: {customer_name}
    Previous Interactions: {previous_interactions}

    Customer Email:
    {email_content}

    Response:
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=200,
        temperature=0.7
    )
    reply = response['choices'][0]['message']['content']
    return reply

# Example usage
# email_content = "I haven't received my order yet, and it's been over two weeks!"
# customer_name = "John Doe"
# previous_interactions = "Order delayed due to stock issues."

# reply = generate_response(email_content, customer_name, previous_interactions)
# print(f"Generated Reply:\n\n{reply}")