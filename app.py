"""
Email Scam Classifier - Flask Web Application
Main application file that handles routing and predictions
"""

from flask import Flask, render_template, request, jsonify
from model import classify_email, get_prediction_confidence
import time

# Initialize Flask app
app = Flask(__name__)

# Configuration
app.config['JSON_SORT_KEYS'] = False
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True


@app.route('/')
def index():
    """
    Render the main page
    
    Returns:
        HTML: The main index page with email classification form
    """
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def predict():
    """
    Handle email classification prediction
    
    Accepts JSON with 'email_text' field
    Returns JSON with 'prediction' and 'confidence'
    
    Returns:
        JSON: {
            'prediction': 'Scam' or 'Not Scam',
            'confidence': float (0.0 to 1.0)
        }
    """
    try:
        # Get JSON data from request
        data = request.get_json()
        
        # Validate input
        if not data:
            return jsonify({
                'error': 'No data provided'
            }), 400
        
        email_text = data.get('email_text', '').strip()
        
        # Check if email text is empty
        if not email_text:
            return jsonify({
                'error': 'Email text is required'
            }), 400
        
        # Check minimum length
        if len(email_text) < 10:
            return jsonify({
                'error': 'Email text is too short. Please provide at least 10 characters.'
            }), 400
        
        # Simulate processing time for realistic UX
        # (Remove or reduce this in production)
        time.sleep(1)
        
        # Get prediction with real confidence score from the model
        prediction, confidence = get_prediction_confidence(email_text)
        
        # Log prediction (optional, for debugging)
        print(f"📧 Prediction: {prediction} (Confidence: {confidence:.4f})")
        
        # Return successful prediction
        return jsonify({
            'prediction': prediction,
            'confidence': confidence
        }), 200
    
    except ValueError as ve:
        # Handle validation errors
        return jsonify({
            'error': f'Validation error: {str(ve)}'
        }), 400
    
    except Exception as e:
        # Handle unexpected errors
        print(f"❌ Error in /predict endpoint: {e}")
        return jsonify({
            'error': 'An error occurred while processing your request. Please try again.'
        }), 500


@app.route('/health')
def health():
    """
    Health check endpoint
    Useful for monitoring if the app is running
    
    Returns:
        JSON: Status information
    """
    from model import get_model_info
    
    model_info = get_model_info()
    
    return jsonify({
        'status': 'healthy',
        'model_loaded': model_info['model_loaded'],
        'model_type': model_info['model_type']
    }), 200


@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'error': 'Endpoint not found'
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'error': 'Internal server error'
    }), 500


# Run the application
if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 STARTING EMAIL SCAM CLASSIFIER")
    print("="*60)
    print("📍 Server: http://127.0.0.1:5000")
    print("🔍 Health Check: http://127.0.0.1:5000/health")
    print("="*60 + "\n")
    
    # Run Flask app
    # use_reloader=False fixes the EmailPreprocessor import issue
    # Set to True if you want auto-reload (but may cause import errors)
    app.run(
        debug=True,
        host='127.0.0.1',
        port=5000,
        use_reloader=False  # Important: Prevents import issues with custom classes
    )