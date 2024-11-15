from flask import Flask, request, render_template
import pickle
import numpy as np

app = Flask(__name__)

# Load the model
with open('model/diabetes_model.pkl', 'rb') as file:
    model = pickle.load(file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Get the input values from the form
    features = [float(x) for x in request.form.values()]
    final_features = np.array(features).reshape(1,-1)
    
    # Get the prediction probabilities
    probabilities = model.predict_proba(final_features)[0]
    non_diabetic_prob = float(probabilities[0] * 100)
    diabetic_prob = float(probabilities[1] * 100)
    
    # Get the class prediction (0 or 1)
    prediction = model.predict(final_features)[0]
    outcome = "Diabetic" if prediction == 1 else "Non-Diabetic"
    
    return render_template('result.html', 
                           outcome=outcome, 
                           diabetic_prob=diabetic_prob, 
                           non_diabetic_prob=non_diabetic_prob)

if __name__ == "__main__":
    app.run(debug=True)

