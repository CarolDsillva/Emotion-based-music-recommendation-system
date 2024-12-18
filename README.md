# **emuziek - Emotion-Based Music Recommendation System**

![Project Logo](logo.png) <!-- Replace with your logo or remove this line -->

Discover music that resonates with your emotions! **emuziek** leverages advanced emotion detection from images and pairs it with personalized playlists to create an immersive music experience.

---

## **Table of Contents**
- [About the Project](#about-the-project)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Machine Learning Model](#machine-learning-model)
- [Installation](#installation)
- [License](#license)
- [Authors](#authors)
- [Contact](#contact)

---

## **About the Project**
**emuziek** uses **Flask** for backend emotion detection and **React** for the user-friendly frontend. Users can upload images or take pictures, allowing the app to detect emotions and generate a curated Spotify playlist to match their mood.

### Key Objectives
- Enhance user engagement with mood-specific music.
- Provide a seamless and interactive interface.
- Leverage machine learning for accurate emotion detection.

---

## **Features**
- **Emotion Detection**:
  - Upload or capture an image to detect emotions like Happy, Sad, Angry, etc.
  - Emotion confidence scores for transparency.
  
- **Music Recommendations**:
  - Spotify playlists curated based on detected emotions.
  
- **Chatbot Integration**:
  - Emotion guidance and explanations.
  - Personalized playlist suggestions based on user input.

- **Cross-Platform Accessibility**:
  - Mobile-friendly design for access on any device.

---

## **Tech Stack**
- **Frontend**: React, HTML, CSS
- **Backend**: Flask (Python)
- **Machine Learning**: TensorFlow, OpenCV
- **APIs**:
  - Spotify Web API
- **Deployment**: Render (Free Tier)

---

## **Machine Learning Model**
The core of **emuziek** is a CNN-based emotion detection model trained on the [FER 2013 Dataset](https://www.kaggle.com/datasets/msambare/fer2013).  

### **Model Architecture**
- **Input**: 48x48 grayscale images.
- **Convolutional Layers**: Extract spatial features from the image.
- **Pooling Layers**: Downsample feature maps to reduce dimensionality.
- **Fully Connected Layers**: Map high-level features to output classes.
- **Output Layer**: Softmax activation to classify one of seven emotions:
  - Angry, Disgust, Fear, Happy, Sad, Surprise, Neutral.

### **Preprocessing**
- Convert input images to grayscale.
- Resize images to 48x48 pixels.
- Normalize pixel values to [0, 1].

### **Training**
- **Dataset**: FER 2013 Dataset (~35,000 labeled images).
- **Loss Function**: Categorical Cross-Entropy.
- **Optimizer**: Adam.
- **Evaluation Metric**: Accuracy.
- Achieved **~70% accuracy** on the test dataset.

### **Inference**
Once an image is uploaded, the model predicts:
1. **Emotion**: The most probable emotion class.
2. **Confidence**: The likelihood of the prediction, aiding transparency.
---

## **Installation**

### **Prerequisites**
1. Python 3.8+ and pip
2. Node.js and npm
3. Git installed locally

---
## **License**
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---


## **Authors**
- [@mishraaastha08](https://github.com/mishraaastha08)

---
## **Contact**
**Carol Maria Dsilva**  
Email: dsillvacarol@gmail.com
LinkedIn: [Your LinkedIn Profile](https://linkedin.com/in/caroldsillva)  
GitHub: [Your GitHub Profile](https://github.com/CarolDsillva)
