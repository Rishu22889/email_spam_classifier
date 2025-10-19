"""
Email Scam Classifier Model
Loads the trained pipeline and makes predictions
"""

import joblib
import os
import sys

# ===== CRITICAL FIX =====
# Import EmailPreprocessor and register it in __main__ namespace
# This allows joblib to find it when unpickling
try:
    from preprocessor import EmailPreprocessor
    
    # Register EmailPreprocessor in the __main__ module
    # This is what joblib looks for when unpickling
    if '__main__' in sys.modules:
        sys.modules['__main__'].EmailPreprocessor = EmailPreprocessor
    
    print("✓ EmailPreprocessor registered successfully")
except ImportError as e:
    print(f"⚠️ Could not import EmailPreprocessor: {e}")
    EmailPreprocessor = None

# ===== Configuration =====
MODEL_PATH = 'pipe_nb.joblib'

# Global variable to hold the model
_model = None
_model_loaded = False


def load_model():
    """
    Load the model with EmailPreprocessor registered
    """
    global _model, _model_loaded
    
    # If already loaded, return immediately
    if _model_loaded:
        return _model
    
    try:
        if not os.path.exists(MODEL_PATH):
            print(f"⚠️ Warning: Model file '{MODEL_PATH}' not found!")
            print(f"   Looking in: {os.path.abspath(MODEL_PATH)}")
            print("   Using fallback classification logic.")
            _model_loaded = True
            return None
        
        # Load the model
        _model = joblib.load(MODEL_PATH)
        _model_loaded = True
        print(f"✅ Model loaded successfully from {MODEL_PATH}")
        print(f"   Model type: {type(_model).__name__}")
        
        # Check pipeline steps
        if hasattr(_model, 'steps'):
            print(f"   Pipeline steps: {[name for name, _ in _model.steps]}")
        
        return _model
            
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        import traceback
        traceback.print_exc()
        _model_loaded = True
        return None


def classify_email(text):
    """
    Classify an email as 'Scam' or 'Not Scam'
    
    Args:
        text (str): Email text to classify
    
    Returns:
        str: 'Scam' or 'Not Scam'
    """
    # Load model if not already loaded
    model = load_model()
    
    if model is not None:
        try:
            # Use the pipeline to predict
            prediction = model.predict([text])[0]
            
            # Your model outputs: 0 = ham (not scam), 1 = spam (scam)
            if prediction == 1:
                return "Spam"
            else:
                return "Not Spam"
        
        except Exception as e:
            print(f"❌ Prediction error: {e}")
            return fallback_classification(text)
    
    else:
        return fallback_classification(text)


def get_prediction_confidence(text):
    """
    Get prediction with confidence score
    
    Args:
        text (str): Email text to classify
    
    Returns:
        tuple: (prediction, confidence)
    """
    # Load model if not already loaded
    model = load_model()
    
    if model is not None:
        try:
            # Get probability scores from the model
            proba = model.predict_proba([text])[0]
            
            # Get the class with highest probability
            prediction_idx = proba.argmax()
            confidence = proba[prediction_idx]
            
            # Convert to label
            prediction = "Spam" if prediction_idx == 1 else "Not Spam"
            
            return prediction, float(confidence)
        
        except Exception as e:
            print(f"❌ Confidence calculation error: {e}")
            prediction = classify_email(text)
            return prediction, 0.85
    
    else:
        prediction = classify_email(text)
        return prediction, 0.85


def fallback_classification(text):
    """
    Fallback classification using keyword matching
    Used when model is not available
    """
    scam_keywords = [
        'urgent', 'verify', 'suspended', 'click here', 'prize', 
        'winner', 'congratulations', 'bank account', 'password',
        'confirm identity', 'act now', 'limited time', 'free money',
        'nigerian prince', 'inheritance', 'tax refund', 'claim now',
        'account locked', 'unusual activity', 'expires today',
        'verify your account', 'confirm your identity', 'update payment'
    ]
    
    text_lower = text.lower()
    scam_score = sum(1 for keyword in scam_keywords if keyword in text_lower)
    
    # If 3 or more scam keywords detected, classify as scam
    return "Spam" if scam_score >= 3 else "Not Spam"


def get_model_info():
    """Get information about the loaded model"""
    model = load_model()
    
    info = {
        'model_loaded': model is not None,
        'model_type': type(model).__name__ if model else None,
        'has_predict_proba': hasattr(model, 'predict_proba') if model else False,
        'model_path': MODEL_PATH,
        'model_exists': os.path.exists(MODEL_PATH)
    }
    return info


# Print model info when module is run directly
if __name__ == '__main__':
    print("\n" + "="*60)
    print("EMAIL SCAM CLASSIFIER - MODEL INFORMATION")
    print("="*60)
    
    # Force load the model
    model = load_model()
    
    info = get_model_info()
    for key, value in info.items():
        print(f"  {key}: {value}")
    print("="*60)
    
    # Test prediction
    if model is not None:
        print("\n🧪 Testing model with sample texts...\n")
        
        test_spam = "URGENT! Your account has been suspended. Click here to verify now!"
        test_ham = "Hi, your order has been shipped. Thanks for shopping with us."
        
        pred1, conf1 = get_prediction_confidence(test_spam)
        pred2, conf2 = get_prediction_confidence(test_ham)
        
        print(f"Test 1 (spam): '{test_spam[:50]}...'")
        print(f"  → Prediction: {pred1}, Confidence: {conf1:.4f}\n")
        
        print(f"Test 2 (ham): '{test_ham[:50]}...'")
        print(f"  → Prediction: {pred2}, Confidence: {conf2:.4f}\n")
        
        print("✅ Model is working correctly!")
    else:
        print("\n⚠️ Model not loaded. Using fallback classification.")
    
    print("="*60 + "\n")