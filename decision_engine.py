class DecisionEngine:
    def __init__(self, rules):
        self.rules = rules

    def decide(self, email_data):
        for rule in self.rules:
            action = rule.check(email_data)
            if action:
                return action
        return 'escalate_to_human'

# Define individual rules
class Rule:
    def check(self, email_data):
        raise NotImplementedError

class AutoReplyRule(Rule):
    def check(self, email_data):
        if email_data['classification'] == 'General Inquiry' and email_data['sentiment'] == 'positive':
            return 'auto_reply'
        return None

class ForwardToBillingRule(Rule):
    def check(self, email_data):
        if email_data['classification'] == 'Billing':
            return 'forward_to_billing'
        return None

class EscalateComplaintRule(Rule):
    def check(self, email_data):
        if email_data['classification'] == 'Complaint' or email_data['sentiment'] == 'negative':
            return 'escalate_to_manager'
        return None

# Initialize the rules and the engine
# rules = [
#     AutoReplyRule(),
#     ForwardToBillingRule(),
#     EscalateComplaintRule(),
# ]

# engine = DecisionEngine(rules)

# Example email data from AI Analysis Module
# email_data = {
#     'classification': 'Billing',
#     'sentiment': 'neutral',
#     'language': 'English',
#     'summary': 'Customer is asking about their invoice.',
#     'content': '...'
# }

# # Decide the next action
# action = engine.decide(email_data)
# print(f"Next action: {action}")