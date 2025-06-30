// DOM Elements
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const generateBtn = document.getElementById('generateBtn');
const loading = document.getElementById('loading');
const result = document.getElementById('result');
const resultImage = document.getElementById('resultImage');
const captionText = document.getElementById('captionText');
const previewImage = document.getElementById('previewImage');
const processedCount = document.getElementById('processedCount');
const avgTime = document.getElementById('avgTime');

// State variables
let selectedFile = null;
let processedImages = 0;
let totalTime = 0;

// Drag and drop functionality
uploadArea.addEventListener('dragover', (e) => {
    e.preventDefault();
    uploadArea.classList.add('dragover');
});

uploadArea.addEventListener('dragleave', () => {
    uploadArea.classList.remove('dragover');
});

uploadArea.addEventListener('drop', (e) => {
    e.preventDefault();
    uploadArea.classList.remove('dragover');
    const files = e.dataTransfer.files;
    if (files.length > 0) {
        handleFile(files[0]);
    }
});

uploadArea.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', (e) => {
    if (e.target.files.length > 0) {
        handleFile(e.target.files[0]);
    }
});

generateBtn.addEventListener('click', () => {
    if (selectedFile) {
        generateCaption(selectedFile);
    }
});

function handleFile(file) {
    if (!file.type.startsWith('image/')) {
        showError('Please select an image file');
        return;
    }

    selectedFile = file;
    
    // Show preview
    const reader = new FileReader();
    reader.onload = (e) => {
        previewImage.src = e.target.result;
        previewImage.style.display = 'block';
    };
    reader.readAsDataURL(file);

    // Show generate button
    generateBtn.style.display = 'inline-block';
    
    // Hide previous results
    result.style.display = 'none';
}

function generateCaption(file) {
    const startTime = Date.now();
    const formData = new FormData();
    formData.append('file', file);

    // Show loading
    loading.style.display = 'block';
    generateBtn.disabled = true;
    result.style.display = 'none';

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        const endTime = Date.now();
        const processingTime = (endTime - startTime) / 1000;
        
        loading.style.display = 'none';
        generateBtn.disabled = false;

        if (data.success) {
            // Update stats
            processedImages++;
            totalTime += processingTime;
            processedCount.textContent = processedImages;
            avgTime.textContent = (totalTime / processedImages).toFixed(1) + 's';

            // Show result
            resultImage.src = 'data:image/png;base64,' + data.image;
            captionText.textContent = data.caption;
            result.style.display = 'block';
            
            // Add success animation
            result.style.animation = 'none';
            result.offsetHeight; // Trigger reflow
            result.style.animation = 'slideInUp 0.6s ease-out';
        } else {
            showError(data.error || 'An error occurred');
        }
    })
    .catch(error => {
        loading.style.display = 'none';
        generateBtn.disabled = false;
        showError('Network error: ' + error.message);
    });
}

function showError(message) {
    const errorDiv = document.createElement('div');
    errorDiv.className = 'error';
    errorDiv.innerHTML = `<i class="fas fa-exclamation-triangle"></i> ${message}`;
    
    // Remove previous errors
    const existingErrors = document.querySelectorAll('.error');
    existingErrors.forEach(err => err.remove());
    
    // Add new error
    uploadArea.parentNode.insertBefore(errorDiv, uploadArea.nextSibling);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

// Check if server is healthy on page load
fetch('/health')
    .then(response => response.json())
    .then(data => {
        if (!data.models_loaded) {
            showError('Server is not ready. Models are still loading...');
        }
    })
    .catch(error => {
        console.log('Health check failed:', error);
    });

// Add some interactive effects
document.addEventListener('DOMContentLoaded', () => {
    // Add floating animation to some elements
    const elements = document.querySelectorAll('.upload-icon, .btn');
    elements.forEach(el => {
        el.classList.add('floating');
    });
}); 