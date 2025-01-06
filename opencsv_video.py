import cv2
import torch
from ultralytics import YOLO
from paddleocr import PaddleOCR
from datetime import datetime, timedelta
from util import read_license_plate
import os

# license plate detector
path = "./static/models/license_plate_detector.pt"
model = YOLO(path)


reader = PaddleOCR(use_angle_cls=True, lang='en')

cap = cv2.VideoCapture(0) 
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# all license plate data
license_plate_data = []

# Method to process each frame and detect license plates
def detect_license_plate(frame):
    global license_plate_data
    
    # detect license plate
    results = model(frame)
    detections = results[0].boxes

    for box in detections:
        # bounding box coordinates
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        conf = box.conf[0]
        cls = int(box.cls[0]) 

        # detected license plate region
        license_plate_region = frame[y1:y2, x1:x2]
        
        # read the text from the license plate
        result = reader.ocr(license_plate_region, cls=True) 

        if result:
            # check and convert text into license plate format
            detected_text = read_license_plate(result[0])
            
            if detected_text is not None:
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

                label = f"{detected_text}" 
                cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)
                
                current_time = datetime.now()

                # check if the license plate already exists within the last 5 minutes
                exists = False
                for entry in license_plate_data:
                    if entry["license_plate"] == detected_text:
                        previous_timestamp = datetime.strptime(entry["timestamp"], "%Y-%m-%d %H:%M:%S")
                        if current_time - previous_timestamp < timedelta(minutes=5):
                            exists = True
                            break 

                if not exists:
                    timestamp = current_time.strftime("%Y-%m-%d %H:%M:%S") 
                    
                    save_dir = "static/plates"
                    if not os.path.exists(save_dir):
                        os.makedirs(save_dir) 
                    
                    # save license plate image file
                    sanitized_timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S").replace(":", "-")
                    sanitized_detected_text = detected_text.replace(" ", "_")
                    filename = f"{save_dir}/license_plate_{sanitized_detected_text}_{sanitized_timestamp}.jpg"
                    cv2.imwrite(filename, frame)
                    
                    # save all data to license plate data
                    license_plate_data.append({"license_plate": detected_text, "timestamp": timestamp, "file_path": filename})
                    print(f"Added license plate: {detected_text}")
                else:
                    print(f"License plate '{detected_text}' already exists within the last 5 minutes.")
                

    return frame

# streaming frames
def generate_frames():
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # feed the frame to detect license plate
        processed_frame = detect_license_plate(frame)
        
        ret, buffer = cv2.imencode('.jpg', processed_frame)
        if not ret:
            continue
        frame = buffer.tobytes()

        # yield the frame as part of the HTTP response to stream it
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

# cleaning directory
def clean_directory(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error deleting file {file_path}: {e}")

# delete all license plate data
def delete_license_plate_data():
    global license_plate_data
    license_plate_data = []
    clean_directory("static/plates")
    return license_plate_data

# delete a row/index in license plate data
def delete_license_plate_row(license_plate):
    global license_plate_data
    entry_to_delete = next((entry for entry in license_plate_data if entry['file_path'] == license_plate), None)
    
    if entry_to_delete:
        # delete the file from the file system
        file_path = entry_to_delete.get('file_path')
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
        
        # remove data
        license_plate_data = [entry for entry in license_plate_data if entry['file_path'] != license_plate]
        return True
    
    return False

def get_license_plate_data():
    global license_plate_data
    return license_plate_data
