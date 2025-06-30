import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import pickle
import os
import glob

def test_multiple_images():
    """Test the model with multiple images to identify patterns"""
    
    # Load models
    model_path = "models/model.keras"
    tokenizer_path = "models/tokenizer.pkl"
    feature_extractor_path = "models/feature_extractor.keras"
    
    print("Loading models...")
    caption_model = load_model(model_path, compile=False)
    feature_extractor = load_model(feature_extractor_path, compile=False)
    
    with open(tokenizer_path, "rb") as f:
        tokenizer = pickle.load(f)
    
    # Get all test images
    test_images = glob.glob("static/images/*.png")
    print(f"Found {len(test_images)} test images")
    
    for img_path in test_images:
        print(f"\n{'='*50}")
        print(f"Testing: {os.path.basename(img_path)}")
        print(f"{'='*50}")
        
        try:
            # Preprocess the image
            img = load_img(img_path, target_size=(224, 224))
            img = img_to_array(img) / 255.0
            img = np.expand_dims(img, axis=0)
            
            # Extract features
            image_features = feature_extractor.predict(img, verbose=0)
            
            # Generate caption
            max_length = 34
            in_text = "startseq"
            generated_words = []
            
            for i in range(max_length):
                sequence = tokenizer.texts_to_sequences([in_text])[0]
                sequence = pad_sequences([sequence], maxlen=max_length)
                yhat = caption_model.predict([image_features, sequence], verbose=0)
                
                # Get top 3 predictions
                top_indices = np.argsort(yhat[0])[-3:][::-1]
                top_words = [tokenizer.index_word.get(idx, f"UNK_{idx}") for idx in top_indices]
                top_probs = [yhat[0][idx] for idx in top_indices]
                
                print(f"Step {i+1}: Top 3: {list(zip(top_words, [f'{p:.4f}' for p in top_probs]))}")
                
                yhat_index = np.argmax(yhat)
                word = tokenizer.index_word.get(yhat_index, None)
                
                if word is None:
                    print(f"Word not found for index {yhat_index}")
                    break
                    
                generated_words.append(word)
                in_text += " " + word
                
                if word == "endseq":
                    break
            
            caption = in_text.replace("startseq", "").replace("endseq", "").strip()
            print(f"\nFinal caption: '{caption}'")
            print(f"Generated words: {generated_words}")
            
        except Exception as e:
            print(f"Error processing {img_path}: {str(e)}")

def analyze_vocabulary():
    """Analyze the vocabulary to understand potential issues"""
    tokenizer_path = "models/tokenizer.pkl"
    
    with open(tokenizer_path, "rb") as f:
        tokenizer = pickle.load(f)
    
    print(f"\n{'='*50}")
    print("VOCABULARY ANALYSIS")
    print(f"{'='*50}")
    
    print(f"Total vocabulary size: {len(tokenizer.word_index)}")
    
    # Check for common words that might be missing
    common_words = [
        'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
        'cat', 'dog', 'bird', 'car', 'tree', 'house', 'person', 'man', 'woman', 'child',
        'sitting', 'standing', 'running', 'walking', 'playing', 'eating', 'drinking',
        'red', 'blue', 'green', 'yellow', 'black', 'white', 'brown', 'gray'
    ]
    
    missing_words = []
    found_words = []
    
    for word in common_words:
        if word in tokenizer.word_index:
            found_words.append(word)
        else:
            missing_words.append(word)
    
    print(f"\nFound words ({len(found_words)}): {found_words}")
    print(f"Missing words ({len(missing_words)}): {missing_words}")
    
    # Check word frequency
    print(f"\nMost common words (top 20):")
    sorted_words = sorted(tokenizer.word_index.items(), key=lambda x: x[1])
    for word, idx in sorted_words[:20]:
        print(f"  {idx}: {word}")
    
    print(f"\nLeast common words (last 20):")
    for word, idx in sorted_words[-20:]:
        print(f"  {idx}: {word}")

if __name__ == "__main__":
    test_multiple_images()
    analyze_vocabulary() 