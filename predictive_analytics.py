# import pandas as pd
# from sklearn.model_selection import train_test_split
# from sklearn.ensemble import RandomForestClassifier

# # Load historical data
# # data = pd.read_csv('customer_interactions.csv')
# data=['sentiment':'positive','email_count':3,'avg_response_time':5.5]
# # Feature Engineering
# data['sentiment_score'] = data['sentiment'].map({'positive': 1, 'neutral': 0, 'negative': -1})
# features = data[['email_count', 'avg_response_time', 'sentiment_score']]
# labels = data['churn_risk']

# # Train/Test Split
# X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.2)

# # Model Training
# model = RandomForestClassifier()
# model.fit(X_train, y_train)

# # Prediction Function
# def predict_churn_risk(customer_data):
#     features = [[
#         customer_data['email_count'],
#         customer_data['avg_response_time'],
#         customer_data['sentiment_score']
#     ]]
#     risk = model.predict(features)
#     return risk[0]

# # Example usage
# customer_data = {
#     'email_count': 5,
#     'avg_response_time': 2.5,
#     'sentiment_score': -1
# }

# risk = predict_churn_risk(customer_data)
# print(f"Churn Risk: {'High' if risk else 'Low'}")


import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier


data = pd.DataFrame([
    {'sentiment': 'positive', 'email_count': 3, 'avg_response_time': 5.5, 'churn_risk': 0},
    {'sentiment': 'negative', 'email_count': 5, 'avg_response_time': 8.0, 'churn_risk': 1},
    {'sentiment': 'neutral', 'email_count': 2, 'avg_response_time': 3.5, 'churn_risk': 0},
    {'sentiment': 'positive', 'email_count': 7, 'avg_response_time': 2.0, 'churn_risk': 0},
    {'sentiment': 'negative', 'email_count': 4, 'avg_response_time': 7.0, 'churn_risk': 1},
])


data['sentiment_score'] = data['sentiment'].map({'positive': 1, 'neutral': 0, 'negative': -1})
features = data[['email_count', 'avg_response_time', 'sentiment_score']]
labels = data['churn_risk']


X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.8)

# Model Training
model = RandomForestClassifier()
model.fit(X_train, y_train)


def predict_churn_risk(customer_data):
    features = [[
        customer_data['email_count'],
        customer_data['avg_response_time'],
        customer_data['sentiment_score']
    ]]
    risk = model.predict(features)
    print(risk[0])
    return risk

# Example usage
customer_data = {
    'email_count': 50,
    'avg_response_time': 12.5,
    'sentiment_score': -1
}

risk = predict_churn_risk(customer_data)
print(f"Churn Risk: {'High' if risk else 'Low'}")
