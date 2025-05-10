# AI-Driven-Waste-Segregation-System
This project leverages Flask and Keras to create a real-time waste classification system using a webcam. The system identifies different types of waste (e.g., recyclables, organic, hazardous) and communicates the results to an ESP32 microcontroller for further action (e.g., sorting).

Features
Real-time Detection: Uses a pre-trained Keras model to classify waste from webcam input.
Confidence Thresholding: Only considers predictions above a set confidence level (e.g., 60%).
ESP32 Integration: Sends detected waste type to an ESP32 via UDP for physical sorting.
Web Interface: Provides a simple Flask-based web app to display detection results.
Setup
Prerequisites:

Python 3.x
Flask (pip install flask)
OpenCV (pip install opencv-python)
Keras/TensorFlow (pip install tensorflow keras)
Run the Application:

bash
python app.py
The Flask server will start at http://0.0.0.0:5000.

ESP32 Configuration:

File Structure
app.py: Main Flask application with detection logic.
keras_Model.h5: Pre-trained Keras model for waste classification.
labels.txt: List of waste classes the model can identify.
templates/index.html: Web interface template (if applicable).
Future Enhancements
Improve model accuracy with more training data.
Add support for multiple waste categories.
Implement a dashboard for analytics.
