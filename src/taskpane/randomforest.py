import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import export_graphviz
import pydot
import re
import win32com.client

def preprocess_email_content(email_content):
    preprocessed_content = email_content.lower()
    return preprocessed_content

def get_current_email():
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    explorer = outlook.Application.ActiveExplorer()
    selection = explorer.Selection
    if len(selection) == 1:
        email = selection.Item(1)
        return email.Subject + " " + email.Body
    else:
        raise Exception("No email is currently open or more than one email is selected.")

# Add transform_email_to_features function here
def transform_email_to_features(preprocessed_email_content):
    # Initialize a list to store the extracted features
    email_features = []

    # Extract NumDots from preprocessed_email_content
    num_dots = preprocessed_email_content.count(".")
    email_features.append(num_dots)

    # Extract NumDash from preprocessed_email_content
    num_dash = preprocessed_email_content.count("-")
    email_features.append(num_dash)

    # Extract NumUnderscore from preprocessed_email_content
    num_underscore = preprocessed_email_content.count("_")
    email_features.append(num_underscore)

    # Extract NumPercent from preprocessed_email_content
    num_percent = preprocessed_email_content.count("%")
    email_features.append(num_percent)

    # Extract NumAmpersand from preprocessed_email_content
    num_ampersand = preprocessed_email_content.count("&")
    email_features.append(num_ampersand)

    # Extract NumHash from preprocessed_email_content
    num_hash = preprocessed_email_content.count("#")
    email_features.append(num_hash)

    # Extract NumNumericChars from preprocessed_email_content
    num_numeric_chars = sum(c.isdigit() for c in preprocessed_email_content)
    email_features.append(num_numeric_chars)

    while len(email_features) != 49:
        email_features.append(num_hash)

    # ...
    # Extract the remaining features based on your specific dataset and requirements
    # email_features.append(feature_x)

    # Combine the extracted features into a numpy array
    email_features = np.array(email_features)

    return email_features



# Load and preprocess the dataset
features = pd.read_csv('Phishing_Legitimate_full.csv')
features = pd.get_dummies(features)

labels = np.array(features['id'])
features = features.drop('id', axis=1)
feature_list = list(features.columns)
features = np.array(features)

train_features, test_features, train_labels, test_labels = train_test_split(features, labels, test_size=0.25, random_state=42)
# Train the RandomForest model
rf = RandomForestRegressor(n_estimators=1000, random_state=42)
rf.fit(train_features, train_labels)

# Get the currently open email in Outlook
email_content = "What the hell is going on"#get_current_email()
print("Current email content: " + email_content)

# Preprocess the email content
print("Switching email to lowercase...")
preprocessed_email_content = preprocess_email_content(email_content)
print("Processed email: " + preprocessed_email_content)

# Transform the preprocessed email content into a format compatible with the random forest model
print("Comparing features...")
email_features = transform_email_to_features(preprocessed_email_content)
#print("Email features: " + email_features)

print("Getting Predictions...")
# Predict if the email is a phishing attempt using the random forest model
phishing_prediction = rf.predict(email_features.reshape(1, -1))
print("Phishing detection value: " + str(phishing_prediction))

# Set a threshold for the prediction to classify it as phishing or not
phishing_threshold = 0.5

if phishing_prediction > phishing_threshold:
    print("This email may be a phishing attempt.")
else:
    print("This email seems legitimate.")