**Title**

HR Attrition Prediction System using Machine Learning with Flask Backend and ReactJS Frontend.

**Solution**

Predicts whether an employee is likely to leave (Yes/No).
Shows attrition probability (0–100%).
Generates HR suggestions such as manager check-ins or engagement actions.
Takes employee details from frontend and processes them through an ML model in backend.
Helps HR teams take proactive actions to reduce attrition.

**Algorithms Used**

This project uses a combination (ensemble) of three machine learning algorithms:
Random Forest – Handles complex decision patterns.
Gradient Boosting – Improves accuracy through boosting techniques.
Logistic Regression – Adds interpretability and linear pattern detection.
These three models are combined to produce a more accurate and stable prediction.

**Impact on Companies**

Reduces employee turnover through early risk detection.
Saves hiring, training, and onboarding costs.
Improves employee satisfaction and engagement.
Helps HR teams make data-driven decisions.
Improves overall productivity and retention strategy.

**Frontend Requirements (ReactJS)**

To run the frontend, install:
Node.js
npm (comes with Node)

Installation steps:
cd frontend
npm install
npm start

This will start the React app at http://localhost:3000.

**Backend Requirements (Flask)**

To run the backend, install:
Python 3.9+
Flask
joblib
numpy
pandas
scikit-learn

Installation steps:

cd backend
python -m venv venv
.\venv\Scripts\activate   # Windows
pip install -r requirements.txt
python app.py

This will start the backend server at http://localhost:5000.

**IF BACKEND ERROR APPEARS FOLLOW THE BELOW STEPS** 

*open terminal and run the below commands 
1. cd backend 
2. python -m venv venv 
3. .\venv\Scripts\Activate.ps1 
4. Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass .\venv\Scripts\Activate.ps1 
5. pip install --upgrade pip 
6. pip uninstall scikit-learn -y 
7. pip install scikit-learn==1.6.1  ///make sure it is in the 1.6.1 version 
8. pip show scikit-learn 
9. pip install -r requirements.txt 
10. python app.py 



















