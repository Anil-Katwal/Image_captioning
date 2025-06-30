# AI Image Caption Generator - Flask App

A modern, professional web application that generates descriptive captions for images using advanced deep learning models.

## ✨ Features

- 🖼️ **Drag & Drop Interface**: Intuitive image upload with drag-and-drop functionality
- 🤖 **AI-Powered Captions**: Uses trained deep learning models for intelligent caption generation
- 🎨 **Modern UI**: Beautiful, responsive design with smooth animations and glass morphism
- ⚡ **Fast Performance**: Models are loaded once and cached for optimal performance
- 📱 **Mobile Responsive**: Perfect experience on desktop and mobile devices
- 📊 **Real-time Statistics**: Track processing time and image count
- 🔧 **Professional Structure**: Well-organized codebase with proper separation of concerns

## 📁 Project Structure

```
Image_caption/
├── app.py                     # Main Flask application
├── main.py                   # Original Streamlit app (for reference)
├── requirements.txt          # Python dependencies
├── README.md                # This documentation
│
├── models/                  # AI Model Files
│   ├── model.keras          # Trained caption model (51MB)
│   ├── feature_extractor.keras # Feature extraction model (72MB)
│   └── tokenizer.pkl        # Text tokenizer (340KB)
│
├── templates/               # HTML Templates
│   └── index.html          # Main web interface
│
├── static/                  # Static Assets
│   ├── css/
│   │   └── style.css       # Main stylesheet
│   ├── js/
│   │   └── app.js          # JavaScript functionality
│   └── images/             # Sample images and assets
│       ├── img_1.png
│       ├── img_2.png
│       └── img_3.png
│
├── uploads/                 # Temporary upload directory
├── logs/                    # Application logs
│   └── app.log             # Log file
│
└── computer-and-nlp-project.ipynb  # Original Jupyter notebook
```

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- TensorFlow 2.x
- All model files in the `models/` directory

### Setup

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Verify model files are present**:
   ```bash
   ls models/
   # Should show: model.keras, feature_extractor.keras, tokenizer.pkl
   ```

## 🎯 Usage

### Running the Flask App

1. **Start the server**:
   ```bash
   python app.py
   ```

2. **Open your browser** and go to:
   ```
   http://localhost:5001
   ```

3. **Upload an image**:
   - Drag and drop an image onto the upload area, or
   - Click the upload area to browse and select a file

4. **Generate caption**:
   - Click the "Generate Caption" button
   - Wait for the AI to process your image
   - View the generated caption and image with overlay

### API Endpoints

- `GET /` - Main web interface
- `POST /upload` - Upload image and generate caption
- `GET /health` - Health check endpoint
- `GET /static/images/<filename>` - Serve static images

## 🏗️ Architecture

### Backend (Flask)
- **Model Management**: Efficient loading and caching of AI models
- **Image Processing**: Optimized image preprocessing and feature extraction
- **Caption Generation**: Sequential word-by-word caption generation
- **Error Handling**: Comprehensive error handling with logging
- **File Management**: Secure file upload and cleanup

### Frontend (HTML/CSS/JS)
- **Modern Design**: Glass morphism, gradients, and smooth animations
- **Responsive Layout**: Mobile-first design approach
- **Interactive Elements**: Drag-and-drop, hover effects, loading states
- **Real-time Feedback**: Progress indicators and error messages
- **Statistics Dashboard**: Processing time and image count tracking

## 🔧 Configuration

### Environment Variables
- `UPLOAD_FOLDER`: Directory for temporary uploads (default: `uploads/`)
- `MAX_CONTENT_LENGTH`: Maximum file size (default: 16MB)

### Model Parameters
- `max_length`: Maximum caption length (default: 34 words)
- `img_size`: Input image size (default: 224x224 pixels)

## 📊 Performance Optimizations

- **Model Caching**: Models loaded once at startup and cached in memory
- **Async Processing**: Non-blocking image processing and caption generation
- **File Cleanup**: Automatic cleanup of temporary upload files
- **Memory Management**: Efficient matplotlib backend configuration
- **Error Recovery**: Graceful error handling and user feedback

## 🛠️ Development

### Adding New Features

1. **Backend Changes**: Modify `app.py` for new API endpoints
2. **Frontend Changes**: Update `templates/index.html` for UI changes
3. **Styling**: Edit `static/css/style.css` for design modifications
4. **Functionality**: Modify `static/js/app.js` for new interactions

### Customization

- **UI Colors**: Modify CSS variables in `static/css/style.css`
- **Model Parameters**: Adjust parameters in `app.py`
- **File Upload**: Change `MAX_CONTENT_LENGTH` in `app.py`
- **Logging**: Configure logging in `app.py`

## 🐛 Troubleshooting

### Common Issues

1. **"Models not loaded properly"**
   - Ensure all model files are in the `models/` directory
   - Check file permissions
   - Verify TensorFlow installation

2. **"Server is not ready"**
   - Wait for models to finish loading (first startup takes longer)
   - Check console output for loading progress
   - Verify port 5001 is available

3. **Upload errors**
   - Ensure image file is valid (JPG, PNG, JPEG)
   - Check file size (max 16MB)
   - Verify internet connection

4. **Matplotlib errors**
   - App uses 'Agg' backend to avoid GUI issues
   - Check logs for detailed error messages

### Performance Tips

- **First Run**: Initial model loading may take 30-60 seconds
- **Subsequent Runs**: Much faster as models are cached
- **Memory Usage**: App uses ~200MB RAM when models are loaded
- **Processing Time**: Average 2-5 seconds per image

## 📝 Logging

The application logs all activities to `logs/app.log`:
- Model loading status
- File uploads and processing
- Error messages and debugging info
- Performance metrics

## 🔒 Security

- **File Validation**: Only image files are accepted
- **Secure Filenames**: Uploaded files get unique, secure names
- **Size Limits**: Maximum file size enforced
- **Temporary Storage**: Files are automatically cleaned up
- **Error Handling**: No sensitive information exposed in errors

## 📱 Browser Compatibility

- Chrome 80+
- Firefox 75+
- Safari 13+
- Edge 80+
- Mobile browsers (iOS Safari, Chrome Mobile)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is for educational and research purposes.

## 🆘 Support

For issues or questions:
1. Check the troubleshooting section
2. Review the logs in `logs/app.log`
3. Verify all dependencies are installed
4. Ensure model files are present and accessible

## 🚀 Future Enhancements

- [ ] Batch processing for multiple images
- [ ] Caption editing and customization
- [ ] Export functionality (PDF, text)
- [ ] User authentication and history
- [ ] API rate limiting and caching
- [ ] Docker containerization
- [ ] Cloud deployment support 