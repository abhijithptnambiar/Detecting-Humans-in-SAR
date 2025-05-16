import cv2
import os
from DBConnection import Db
from pygame import mixer
import time
import numpy as np
import datetime

# Paths for YOLO model files
yolo_cfg = r"C:\Users\User\Downloads\Detect_Hu_In_SAR\Detect_Hu_In_SAR\Detect_Hu_In_SAR_app\static\yolo_files\yolo.cfg"
yolo_weights = r"C:\Users\User\Downloads\Detect_Hu_In_SAR\Detect_Hu_In_SAR\Detect_Hu_In_SAR_app\static\yolo_files\yolo.weights"
coco_names = r"C:\Users\User\Downloads\Detect_Hu_In_SAR\Detect_Hu_In_SAR\Detect_Hu_In_SAR_app\static\yolo_files\coco.names"

# Load YOLO model
net = cv2.dnn.readNet(yolo_weights, yolo_cfg)
layer_names = net.getLayerNames()
output_layers = [layer_names[i - 1] for i in net.getUnconnectedOutLayers().flatten()]

# Load COCO labels
with open(coco_names, "r") as f:
    classes = [line.strip() for line in f.readlines()]

# Static path
staticpath = r"C:\Users\User\Downloads\Detect_Hu_In_SAR\Detect_Hu_In_SAR\Detect_Hu_In_SAR_app\static"


cam = cv2.VideoCapture(r"C:\Users\User\Downloads\Detect_Hu_In_SAR\Detect_Hu_In_SAR\Detect_Hu_In_SAR_app\static\3545736297-preview.mp4")
currentframe = 0






# Define the directory for saving detected frames
detection_folder = os.path.join(staticpath, "detections")
os.makedirs(detection_folder, exist_ok=True)  # Ensure directory exists

db = Db()

# Initialize last saved time
last_saved_time = 0


def play_alert_sound():
    """Play alert sound when human is detected."""
    mixer.init()
    mixer.music.load(os.path.join(staticpath, 'attack2t22wav-14511.mp3'))
    mixer.music.play()
    time.sleep(5)
    mixer.music.stop()


def detect_humans(frame):
    """Detect humans in the given frame using YOLO."""
    height, width, _ = frame.shape
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (416, 416), (0, 0, 0), True, crop=False)
    net.setInput(blob)
    outs = net.forward(output_layers)

    class_ids = []
    confidences = []
    boxes = []
    human_detected = False

    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]

            if confidence > 0.5 and classes[class_id] == "person":
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)
                human_detected = True

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
    if len(indexes) > 0:
        for i in indexes.flatten():
            x, y, w, h = boxes[i]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            label = f"{classes[class_ids[i]]}: {confidences[i]:.2f}"
            cv2.putText(frame, label, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    return human_detected, frame


def process_uploaded_video(video_path):
    """Process an uploaded video for human detection."""
    global last_saved_time
    cam = cv2.VideoCapture(video_path)
    frame_count = 0
    start_time = time.time()

    while cam.isOpened():
        if time.time() - start_time > 60:
            print("Stopping video processing after 1 minute.")
            break  # Stop processing after 1 minute

        ret, frame = cam.read()
        if not ret:
            break  # Stop when the video ends

        human_detected, frame_with_detections = detect_humans(frame)

        if human_detected:
            cv2.putText(frame_with_detections, "ALERT: Human Detected!", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1,
                        (0, 0, 255), 2)

            # Save frame only if 2 seconds have passed since the last save
            current_time = time.time()
            if current_time - last_saved_time > 2:
                last_saved_time = current_time
                frame_image_filename = f"a_{frame_count}.jpg"  # Only filename
                frame_image_path = os.path.join(detection_folder, frame_image_filename)  # Full path in project
                cv2.imwrite(frame_image_path, frame_with_detections)
                print(f"Human detected, frame saved at {frame_image_path}")

                # Insert into database using relative path
                date = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                query = "INSERT INTO Detect_Hu_In_SAR_app_detection (date, image) VALUES (%s, %s)"
                params = (date, f"/static/detections/{frame_image_filename}")  # Save relative path in DB
                db.insert(query, params)

                play_alert_sound()

        cv2.imshow("Human Detection", frame_with_detections)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        frame_count += 1

    cam.release()
    cv2.destroyAllWindows()





