from ultralytics import YOLO
import cv2
import sqlite3
from datetime import datetime

model = YOLO("yolov8n.pt")

# Connect database
conn = sqlite3.connect("traffic.db", check_same_thread=False)
cursor = conn.cursor()

# COCO classes for vehicles
VEHICLES = ["car", "motorcycle", "bus", "truck"]

def run_detection():
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Camera not found")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        results = model(frame)

        boxes = results[0].boxes
        names = model.names

        for box in boxes:
            cls_id = int(box.cls[0])
            class_name = names[cls_id]

            if class_name in VEHICLES:
                cursor.execute(
                    "INSERT INTO vehicles(vehicle_type) VALUES(?)",
                    (class_name,)
                )
                conn.commit()

        frame = results[0].plot()

        cv2.imshow("AI Traffic Detection", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
