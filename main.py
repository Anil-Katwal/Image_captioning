import streamlit as st
import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import matplotlib.pyplot as plt
import pickle
import os

# Cache the model loading to avoid reloading every time
@st.cache_resource
def load_models():
    """Load models and tokenizer once and cache them"""
    try:
        # Update paths to match your current directory structure
        model_path = "model.keras"
        tokenizer_path = "tokenizer.pkl"
        feature_extractor_path = "feature_extractor.keras"
        
        # Check if files exist
        if not os.path.exists(model_path):
            st.error(f"Model file not found: {model_path}")
            return None, None, None
        if not os.path.exists(tokenizer_path):
            st.error(f"Tokenizer file not found: {tokenizer_path}")
            return None, None, None
        if not os.path.exists(feature_extractor_path):
            st.error(f"Feature extractor file not found: {feature_extractor_path}")
            return None, None, None
            
        # Load models with progress indicator
        with st.spinner("Loading caption model..."):
            caption_model = load_model(model_path, compile=False)
        
        with st.spinner("Loading feature extractor..."):
            feature_extractor = load_model(feature_extractor_path, compile=False)
        
        with st.spinner("Loading tokenizer..."):
            with open(tokenizer_path, "rb") as f:
                tokenizer = pickle.load(f)
        
        st.success("All models loaded successfully!")
        return caption_model, feature_extractor, tokenizer
        
    except Exception as e:
        st.error(f"Error loading models: {str(e)}")
        return None, None, None

# Function to generate and display caption
def generate_and_display_caption(image_path, caption_model, feature_extractor, tokenizer, max_length=34, img_size=224):
    if caption_model is None or feature_extractor is None or tokenizer is None:
        st.error("Models not loaded properly. Please check the model files.")
        return

    try:
        # Preprocess the image
        with st.spinner("Processing image..."):
            img = load_img(image_path, target_size=(img_size, img_size))
            img = img_to_array(img) / 255.0  # Normalize pixel values
            img = np.expand_dims(img, axis=0)
            image_features = feature_extractor.predict(img, verbose=0)  # Extract image features

        # Generate the caption
        with st.spinner("Generating caption..."):
            in_text = "startseq"
            for i in range(max_length):
                sequence = tokenizer.texts_to_sequences([in_text])[0]
                sequence = pad_sequences([sequence], maxlen=max_length)
                yhat = caption_model.predict([image_features, sequence], verbose=0)
                yhat_index = np.argmax(yhat)
                word = tokenizer.index_word.get(yhat_index, None)
                if word is None:
                    break
                in_text += " " + word
                if word == "endseq":
                    break
            caption = in_text.replace("startseq", "").replace("endseq", "").strip()

        # Display the image with the generated caption
        img = load_img(image_path, target_size=(img_size, img_size))
        plt.figure(figsize=(8, 8))
        plt.imshow(img)
        plt.axis('off')
        plt.title(caption, fontsize=16, color='blue')
        st.pyplot(plt)  # Display image in Streamlit
        
        # Also display caption as text
        st.success(f"Generated Caption: **{caption}**")
        
    except Exception as e:
        st.error(f"Error generating caption: {str(e)}")

# Streamlit app interface
def main():
    st.set_page_config(
        page_title="Image Caption Generator",
        page_icon="🖼️",
        layout="wide"
    )
    
    st.title("🖼️ Image Caption Generator")
    st.write("Upload an image and generate a caption using the trained model.")
    
    # Load models once at startup
    caption_model, feature_extractor, tokenizer = load_models()
    
    if caption_model is None:
        st.error("Failed to load models. Please ensure all model files are in the correct location.")
        st.stop()

    # Upload the image
    uploaded_image = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        # Save the uploaded image temporarily
        with open("uploaded_image.jpg", "wb") as f:
            f.write(uploaded_image.getbuffer())

        # Generate caption and display image with caption
        generate_and_display_caption("uploaded_image.jpg", caption_model, feature_extractor, tokenizer)
        
        # Clean up temporary file
        if os.path.exists("uploaded_image.jpg"):
            os.remove("uploaded_image.jpg")

if __name__ == "__main__":
    main()
