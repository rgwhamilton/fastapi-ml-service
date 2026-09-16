
import joblib
model = joblib.load("models/sentiment_model.joblib")
def predict(text):
    prediction = model.predict([text])[0]
    confidence = model.predict_proba([text]).max()
    label = "Positive" if prediction == 1 else "Negative"
    return {"prediction": label, "confidence": float(confidence)}
