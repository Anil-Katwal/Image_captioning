from flask import Flask, render_template, request, jsonify, send_file
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import matplotlib
matplotlib.use('Agg')  # Set non-interactive backend to avoid threading issues
import matplotlib.pyplot as plt
import pickle
import os
import base64
from io import BytesIO
import uuid
from werkzeug.utils import secure_filename
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/app.log'),
        logging.StreamHandler()
    ]
)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create necessary directories if they don't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs('logs', exist_ok=True)
os.makedirs('models', exist_ok=True)

# Global variables to store loaded models
caption_model = None
feature_extractor = None
tokenizer = None

def load_models():
    """Load models and tokenizer once at startup"""
    global caption_model, feature_extractor, tokenizer
    
    try:
        # Model paths - updated to use models folder
        model_path = "models/model.keras"
        tokenizer_path = "models/tokenizer.pkl"
        feature_extractor_path = "models/feature_extractor.keras"
        
        # Check if files exist
        if not all(os.path.exists(path) for path in [model_path, tokenizer_path, feature_extractor_path]):
            logging.error("One or more model files not found")
            return False
            
        logging.info("Loading models...")
        caption_model = load_model(model_path, compile=False)
        feature_extractor = load_model(feature_extractor_path, compile=False)
        
        with open(tokenizer_path, "rb") as f:
            tokenizer = pickle.load(f)
            
        logging.info("All models loaded successfully!")
        return True
        
    except Exception as e:
        logging.error(f"Error loading models: {str(e)}")
        return False

def improve_caption(caption):
    """Post-process caption to make it more natural"""
    if not caption:
        return caption
    
    # Add missing articles where appropriate
    words = caption.split()
    improved_words = []
    
    for i, word in enumerate(words):
        # Add 'a' before certain words if not preceded by an article or adjective
        if i > 0 and word in ['dog', 'cat', 'man', 'woman', 'person', 'child', 'boy', 'girl']:
            prev_word = words[i-1].lower()
            # Don't add 'a' if preceded by article, adjective, or number
            if prev_word not in ['a', 'an', 'the', 'this', 'that', 'these', 'those', 'black', 'white', 'brown', 'red', 'blue', 'green', 'yellow', 'gray', 'two', 'three', 'four', 'five']:
                improved_words.append('a')
        improved_words.append(word)
    
    improved_caption = ' '.join(improved_words)
    
    # Capitalize first letter
    if improved_caption:
        improved_caption = improved_caption[0].upper() + improved_caption[1:]
    
    return improved_caption

def generate_caption(image_path, max_length=34, img_size=224, temperature=1.0):
    """Generate caption for the given image with improved prediction"""
    if caption_model is None or feature_extractor is None or tokenizer is None:
        return "Error: Models not loaded properly"
    
    try:
        # Preprocess the image
        img = load_img(image_path, target_size=(img_size, img_size))
        img = img_to_array(img) / 255.0  # Normalize pixel values
        img = np.expand_dims(img, axis=0)
        image_features = feature_extractor.predict(img, verbose=0)  # Extract image features

        # Generate the caption with improved prediction
        in_text = "startseq"
        generated_words = []
        
        for i in range(max_length):
            sequence = tokenizer.texts_to_sequences([in_text])[0]
            sequence = pad_sequences([sequence], maxlen=max_length)
            yhat = caption_model.predict([image_features, sequence], verbose=0)
            
            # Apply temperature sampling for more diverse predictions
            if temperature != 1.0:
                yhat = np.log(yhat) / temperature
                yhat = np.exp(yhat)
                yhat = yhat / np.sum(yhat)
            
            # Get top 5 predictions for debugging
            top_indices = np.argsort(yhat[0])[-5:][::-1]
            top_words = [tokenizer.index_word.get(idx, f"UNK_{idx}") for idx in top_indices]
            top_probs = [yhat[0][idx] for idx in top_indices]
            
            logging.info(f"Step {i+1}: Top 5 predictions: {list(zip(top_words, top_probs))}")
            
            yhat_index = np.argmax(yhat)
            word = tokenizer.index_word.get(yhat_index, None)
            
            if word is None:
                logging.warning(f"Word not found for index {yhat_index}")
                break
                
            generated_words.append(word)
            in_text += " " + word
            
            if word == "endseq":
                break
        
        caption = in_text.replace("startseq", "").replace("endseq", "").strip()
        
        # Improve the caption
        improved_caption = improve_caption(caption)
        
        # Log the generation process
        logging.info(f"Generated words: {generated_words}")
        logging.info(f"Original caption: '{caption}'")
        logging.info(f"Improved caption: '{improved_caption}'")
        
        return improved_caption
        
    except Exception as e:
        logging.error(f"Error generating caption: {str(e)}")
        return f"Error generating caption: {str(e)}"

def create_image_with_caption(image_path, caption, img_size=224):
    """Create an image with the caption overlaid"""
    try:
        img = load_img(image_path, target_size=(img_size, img_size))
        plt.figure(figsize=(6, 6), dpi=100)  # Smaller figure for faster processing
        plt.imshow(img)
        plt.axis('off')
        plt.title(caption, fontsize=14, color='blue', pad=15)
        
        # Save to bytes buffer with optimized settings
        buffer = BytesIO()
        plt.savefig(buffer, format='png', bbox_inches='tight', pad_inches=0.3, dpi=100)
        buffer.seek(0)
        plt.close('all')  # Close all figures to free memory
        
        return buffer
        
    except Exception as e:
        logging.error(f"Error creating image with caption: {str(e)}")
        return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file:
        # Get temperature parameter for prediction diversity
        temperature = float(request.form.get('temperature', 1.0))
        temperature = max(0.1, min(2.0, temperature))  # Clamp between 0.1 and 2.0
        
        # Generate unique filename
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
        
        try:
            # Save uploaded file
            file.save(filepath)
            logging.info(f"File uploaded: {filename} (temperature: {temperature})")
            
            # Generate caption with temperature
            caption = generate_caption(filepath, temperature=temperature)
            
            # Create image with caption
            image_buffer = create_image_with_caption(filepath, caption)
            
            if image_buffer:
                # Convert to base64 for display
                image_base64 = base64.b64encode(image_buffer.getvalue()).decode('utf-8')
                
                # Clean up uploaded file
                os.remove(filepath)
                
                logging.info(f"Caption generated successfully for {filename}")
                return jsonify({
                    'success': True,
                    'caption': caption,
                    'image': image_base64,
                    'temperature': temperature
                })
            else:
                return jsonify({'error': 'Error processing image'}), 500
                
        except Exception as e:
            # Clean up on error
            if os.path.exists(filepath):
                os.remove(filepath)
            logging.error(f"Error processing file {filename}: {str(e)}")
            return jsonify({'error': f'Error processing file: {str(e)}'}), 500
    
    return jsonify({'error': 'Invalid file'}), 400

@app.route('/health')
def health_check():
    """Health check endpoint"""
    models_loaded = all([caption_model, feature_extractor, tokenizer])
    return jsonify({
        'status': 'healthy' if models_loaded else 'unhealthy',
        'models_loaded': models_loaded,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/static/images/<filename>')
def serve_image(filename):
    """Serve static images"""
    return send_file(f'static/images/{filename}')

if __name__ == '__main__':
    # Load models at startup
    if not load_models():
        logging.error("Failed to load models. Exiting...")
        exit(1)
    
    # Get port from environment variable (for Render) or use default
    port = int(os.environ.get('PORT', 5000))
    
    logging.info("Starting Flask app...")
    print(f"Open your browser and go to: http://localhost:{port}")
    app.run(debug=False, host='0.0.0.0', port=port) 