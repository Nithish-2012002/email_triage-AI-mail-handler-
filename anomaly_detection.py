from sklearn.ensemble import IsolationForest

# Example feature: email length, number of links, etc.
def extract_features(email_content):
    print("email content: "+email_content)
    features = {
        'length': len(email_content),
        'num_links': email_content.count('http'),
        # Add more features as needed
    }
    print("features: ",features)
    return features

# Train the model with normal email features
def train_anomaly_detector(normal_emails):
    feature_list = [list(extract_features(email).values()) for email in normal_emails]
    model = IsolationForest(contamination=0.01)
    print(feature_list)
    model.fit(feature_list)
    print(model)
    return model

# Detect anomalies
def is_anomalous(email_content, model):
    features = list(extract_features(email_content).values())
    result = features[1]
    print("result",result)
    return result


