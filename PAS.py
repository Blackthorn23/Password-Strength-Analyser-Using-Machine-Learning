import joblib
import pandas as pd
import re

model = joblib.load("password_strength_model.pkl")

def extract_features(password):
    return {
        "length": len(password),
        "num_uppercase": sum(1 for c in password if c.isupper()),
        "num_lowercase": sum(1 for c in password if c.islower()),
        "num_digits": sum(1 for c in password if c.isdigit()),
        "num_special": sum(1 for c in password if not c.isalnum()),
        "has_repeats": int(bool(re.search(r'(.)\1{2,}', password)))  
    }

def analyze_password(password):
    features = extract_features(password)
    features_df = pd.DataFrame([features]) 
    expected_columns = ["length", "num_uppercase", "num_lowercase", "num_digits", "num_special", "has_repeats"]
    features_df = features_df[expected_columns]  
    prediction = model.predict(features_df)[0]
    strength_label = "Strong Password!" if prediction == 1 else "Weak Password. Try adding more variety."
    return strength_label

def password_analyzer_system():
    print("Welcome to the Password Analyzer System!")
    print("Enter a password to check its strength (or type 'exit' to quit).")
    
    while True:
        password = input("\nEnter a password: ")
        
        if password.lower() == "exit":
            print("Exiting the Password Analyzer System. Goodbye!")
            break
        
        strength = analyze_password(password)
        print(f"The password strength is: {strength}")

if __name__ == "__main__":
    password_analyzer_system()
