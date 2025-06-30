import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import pickle
import os

def test_prediction():
    """Test the prediction function to debug issues"""
    
    # Load models
    model_path = "models/model.keras"
    tokenizer_path = "models/tokenizer.pkl"
    feature_extractor_path = "models/feature_extractor.keras"
    
    print("Loading models...")
    caption_model = load_model(model_path, compile=False)
    feature_extractor = load_model(feature_extractor_path, compile=False)
    
    with open(tokenizer_path, "rb") as f:
        tokenizer = pickle.load(f)
    
    print(f"Vocabulary size: {len(tokenizer.word_index) + 1}")
    print(f"Word index sample: {list(tokenizer.word_index.items())[:10]}")
    
    # Test with a sample image
    test_image_path = "static/images/img_1.png"
    
    if not os.path.exists(test_image_path):
        print(f"Test image not found: {test_image_path}")
        return
    
    print(f"Testing with image: {test_image_path}")
    
    # Preprocess the image
    img = load_img(test_image_path, target_size=(224, 224))
    img = img_to_array(img) / 255.0
    img = np.expand_dims(img, axis=0)
    
    print(f"Image shape: {img.shape}")
    
    # Extract features
    image_features = feature_extractor.predict(img, verbose=0)
    print(f"Image features shape: {image_features.shape}")
    
    # Test prediction step by step
    max_length = 34
    in_text = "startseq"
    
    print(f"Starting with: '{in_text}'")
    
    for i in range(max_length):
        sequence = tokenizer.texts_to_sequences([in_text])[0]
        print(f"Step {i+1}: Sequence: {sequence}")
        
        sequence = pad_sequences([sequence], maxlen=max_length)
        print(f"Step {i+1}: Padded sequence shape: {sequence.shape}")
        
        yhat = caption_model.predict([image_features, sequence], verbose=0)
        print(f"Step {i+1}: Prediction shape: {yhat.shape}")
        print(f"Step {i+1}: Prediction sample: {yhat[0][:10]}")
        
        yhat_index = np.argmax(yhat)
        print(f"Step {i+1}: Predicted index: {yhat_index}")
        
        word = tokenizer.index_word.get(yhat_index, None)
        print(f"Step {i+1}: Predicted word: '{word}'")
        
        if word is None:
            print("Word not found in vocabulary, stopping")
            break
            
        in_text += " " + word
        print(f"Step {i+1}: Updated text: '{in_text}'")
        
        if word == "endseq":
            print("End sequence found, stopping")
            break
    
    caption = in_text.replace("startseq", "").replace("endseq", "").strip()
    print(f"\nFinal caption: '{caption}'")
    
    # Test tokenizer functionality
    print("\n--- Tokenizer Test ---")
    test_text = "startseq a cat sitting"
    print(f"Test text: '{test_text}'")
    sequence = tokenizer.texts_to_sequences([test_text])[0]
    print(f"Sequence: {sequence}")
    
    # Check vocabulary
    print(f"\n--- Vocabulary Check ---")
    print(f"Total words in vocabulary: {len(tokenizer.word_index)}")
    print(f"Index to word mapping size: {len(tokenizer.index_word)}")
    
    # Check for common words
    common_words = ['startseq', 'endseq', 'a', 'the', 'is', 'are', 'cat', 'dog', 'sitting', 'standing']
    for word in common_words:
        if word in tokenizer.word_index:
            print(f"'{word}' -> index {tokenizer.word_index[word]}")
        else:
            print(f"'{word}' -> NOT FOUND")

if __name__ == "__main__":
    test_prediction() 