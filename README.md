# **emuziek - Emotion-Based Music Recommendation System**
![landing page](https://github.com/CarolDsillva/Emotion-based-music-recommendation-system/blob/main/screenshots/1.png)
The project combines advanced machine learning techniques with music recommendation systems to create an immersive and personalized music experience.

---

## **Table of Contents**

- [About the Project](#about-the-project)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [System Architecture](#system-architecture)
- [Machine Learning Model](#machine-learning-model)
- [Installation](#installation)
- [Usage](#usage)
- [Screenshots/Demo](#screenshotsdemo)
- [Contributing](#contributing)
- [License](#license)
- [Authors](#authors)
- [Contact](#contact)

---

## **About the Project**

**emuziek** uses **Flask** for backend emotion detection and **React** for the user-friendly frontend. By analyzing facial expressions from uploaded images, it detects emotions and curates Spotify playlists that align with your mood.

### **Key Features**

- Uses a CNN model to detect emotions like Angry, Disgust, Fear, Happy, Sad, Surprise and Neutral
- It uses the Cosine similarity to find and recommend songs that match the emotion-based features.
- Queries the Spotify API to fetch songs and other information.

---

## **Tech Stack**

- **Frontend**: React, HTML, CSS
- **Backend**: Flask (Python)
- **Machine Learning**: TensorFlow, OpenCV
- **APIs**:
  - Spotify Web API
- **Deployment**: TBD

---

## **System Architecture**

1. **Frontend**:
   - Built using React for a dynamic, responsive and modern UI.
2. **Backend**:
   - Flask REST API processes images and returns emotion predictions.
3. **Machine Learning**:
   - The convolutional neural network (CNN) model was trained on the FER 2013 dataset to classify emotions.
4. **Recommendation System**:
   - Uses cosine similarity and MinMaxScaler for feature-based song recommendations.
5. **Spotify Integration**:
   - Embeds playlists and tracks via Spotify API.

---
## **Machine Learning Model and datasets**
The core of **emuziek** is a CNN-based emotion detection model trained on the [FER 2013 Dataset](https://www.kaggle.com/datasets/msambare/fer2013) and the [Spotify dataset](https://www.kaggle.com/datasets/vatsalmavani/spotify-dataset).  

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


## **Installation**

### **Prerequisites**

- Python 3.8+
- Git installed locally

### **Setup Instructions**

1. Clone the repository:
   ```bash
   git clone https://github.com/CarolDsillva/Emotion-based-music-recommendation-system.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Emotion
   ```
3. Install dependencies:
   ```bash
   # Backend
   cd backend
   pip install -r requirements.txt

   # Frontend
   cd fer
   npm install
   ```
4. Run the project:
   ```bash
   # Backend
   python app.py

   # Frontend
   npm start
   ```
5. Open your browser and navigate to `http://localhost:3000` to use the app.

---

## **Usage**

1. Upload an image on the landing page.
2. Wait for the emotion detection process to complete.
3. View the detected emotion and confidence score.
4. Explore the recommended songs and play them directly via the embedded Spotify player.

---

## **Screenshots/Demo**

- **Landing Page**: ![landing page](https://github.com/CarolDsillva/Emotion-based-music-recommendation-system/blob/main/screenshots/1.png)
- **Emotion Detection Result and music recommendaation**: ![detection page](https://github.com/CarolDsillva/Emotion-based-music-recommendation-system/blob/main/screenshots/2.png)

---

## **Contributing**

We welcome contributions! To contribute:

1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit changes:
   ```bash
   git commit -m "Add feature description"
   ```
4. Push to the branch:
   ```bash
   git push origin feature-name
   ```
5. Open a pull request on GitHub.

---

## **License**

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## **Authors**

- [Carol Maria Dsilva](https://github.com/CarolDsillva)
- [Aastha Mishra](https://github.com/mishraaastha08)
- [Akanksha Singh](https://github.com/snghakanksha)
- [Anushka](https://github.com/Minmin-r)

---

## **Contact**

For questions or feedback:

- **Email**: [dsillvacarol@gmail.com](mailto\:dsillvacarol@gmail.com)
- **LinkedIn**: [Carol Maria Dsilva](https://linkedin.com/in/caroldsillva)
- **GitHub**: [CarolDsillva](https://github.com/CarolDsillva)

