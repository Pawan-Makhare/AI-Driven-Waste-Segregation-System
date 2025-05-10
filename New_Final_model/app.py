from flask import Flask, render_template, jsonify
from keras.models import load_model
import cv2
import numpy as np
import socket

app = Flask(__name__)

# Load AI model
model = load_model("keras_Model.h5", compile=False)
class_names = open("labels.txt", "r").readlines()
confidence_threshold = 0.6

# Initialize webcam
camera = cv2.VideoCapture(0)

# ESP32 details (Replace with actual IP)
ESP32_IP = "192.168.61.151"
ESP32_PORT = 8080
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Variable to store detected waste type
latest_result = {"class": "Detecting...", "confidence": "0%"}

def detect_waste():
    global latest_result

    ret, image = camera.read()
    if not ret:
        return

    # Preprocess the image
    image_resized = cv2.resize(image, (224, 224))
    image_array = np.asarray(image_resized, dtype=np.float32).reshape(1, 224, 224, 3)
    image_array = (image_array / 127.5) - 1  # Normalize

    # Predict
    prediction = model.predict(image_array)
    index = np.argmax(prediction)
    class_name = class_names[index].strip()
    confidence_score = prediction[0][index]

    if confidence_score >= confidence_threshold:
        detected_waste = class_name
        confidence_text = f"{confidence_score * 100:.2f}%"
    else:
        detected_waste = "Unidentified"
        confidence_text = f"{confidence_score * 100:.2f}%"

    # Update latest result
    latest_result = {"class": detected_waste, "confidence": confidence_text}

    # Send data to ESP32
    message = detected_waste.encode()
    client_socket.sendto(message, (ESP32_IP, ESP32_PORT))

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/detect')
def get_detection():
    detect_waste()
    return jsonify(latest_result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
# from flask import Flask, render_template, jsonify  #abc
# from keras.models import load_model
# import cv2
# import numpy as np
# import socket
# import time
#
# app = Flask(__name__)
#
# # Load AI model
# model = load_model("keras_Model.h5", compile=False)
# class_names = open("labels.txt", "r").readlines()
# confidence_threshold = 0.6
#
# # Initialize webcam
# camera = cv2.VideoCapture(0)
#
# # ESP32 details
# ESP32_IP = "192.168.176.151"
# ESP32_PORT = 8080
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# client_socket.settimeout(5)
#
# # Store the latest result
# latest_result = {"class": "Detecting...", "confidence": "0%", "info": ""}
#
# # ✅ Waste information dictionary
# waste_info = {
#     "Plastic": {
#         "description": "Plastic waste includes bottles, wrappers, and packaging. It takes hundreds of years to decompose.",
#         "recycling": "Can be recycled into new bottles, containers, or textiles.",
#         "problems": "Contributes to ocean pollution and microplastic contamination."
#     },
#     "Paper": {
#         "description": "Paper waste consists of newspapers, magazines, and cardboard.",
#         "recycling": "Can be recycled into new paper products.",
#         "problems": "Overuse of paper leads to deforestation."
#     },
#     "Organic": {
#         "description": "Organic waste includes food scraps and plant materials.",
#         "recycling": "Can be composted into natural fertilizer.",
#         "problems": "If not composted, it emits methane gas during decomposition."
#     },
#     "Unidentified": {
#         "description": "The waste type could not be accurately identified.",
#         "recycling": "Unknown recycling potential.",
#         "problems": "Needs manual verification to avoid improper disposal."
#     }
# }
#
# # ✅ Function to wait for ESP32 acknowledgment
# def wait_for_esp32_ack():
#     try:
#         response, _ = client_socket.recvfrom(1024)
#         message = response.decode()
#
#         if message == "Task Completed":
#             print("✅ ESP32 confirmed: Task Completed")
#         else:
#             print(f"⚠️ Unexpected response: {message}")
#
#     except socket.timeout:
#         print("⚠️ No acknowledgment from ESP32. Retrying...")
#         time.sleep(1)
#
# # ✅ Function to detect waste and add general information
# def detect_waste():
#     global latest_result
#
#     ret, image = camera.read()
#     if not ret:
#         return
#
#     # Preprocess the image
#     image_resized = cv2.resize(image, (224, 224))
#     image_array = np.asarray(image_resized, dtype=np.float32).reshape(1, 224, 224, 3)
#     image_array = (image_array / 127.5) - 1
#
#     # Predict
#     prediction = model.predict(image_array)
#     index = np.argmax(prediction)
#     class_name = class_names[index].strip()
#     confidence_score = prediction[0][index]
#
#     if confidence_score >= confidence_threshold:
#         detected_waste = class_name
#         confidence_text = f"{confidence_score * 100:.2f}%"
#     else:
#         detected_waste = "Unidentified"
#         confidence_text = f"{confidence_score * 100:.2f}%"
#
#     # Get general information
#     info = waste_info.get(detected_waste, waste_info["Unidentified"])
#
#     # Update latest result
#     latest_result = {
#         "class": detected_waste,
#         "confidence": confidence_text,
#         "info": info
#     }
#
#     # Send data to ESP32
#     message = detected_waste.encode()
#     client_socket.sendto(message, (ESP32_IP, ESP32_PORT))
#     print(f"📤 Sent waste type: {detected_waste}")
#
#     # Wait for ESP32 to complete task
#     wait_for_esp32_ack()
#
# @app.route('/')
# def home():
#     return render_template("index.html")
#
# @app.route('/detect')
# def get_detection():
#     detect_waste()
#     return jsonify(latest_result)
#
# if __name__ == "__main__":
#     app.run(host="0.0.0.0", port=5000, debug=True)
