import cv2
import numpy as np
import os
import django
from datetime import datetime
import warnings

# Suppress compatibility warnings
warnings.filterwarnings('ignore')
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'face_project.settings')
django.setup()

from recognition.models import PhoneUsageDetection
from django.core.files.base import ContentFile

# Try to import YOLO with error handling
try:
    from ultralytics import YOLO
    YOLO_AVAILABLE = True
except Exception as e:
    print(f"Warning: YOLO import issue - {e}")
    YOLO_AVAILABLE = False

class DjangoMultiDetectionSystem:
    def __init__(self):
        # Create directory for detections if it doesn't exist
        self.detection_dir = 'media/phone_detections'
        os.makedirs(self.detection_dir, exist_ok=True)

        # Load YOLO model with error handling
        if YOLO_AVAILABLE:
            try:
                print("Loading YOLOv8 model...")
                self.yolo_model = YOLO('yolov8n.pt')
                print("✓ Model loaded successfully")
                self.model_loaded = True
            except Exception as e:
                print(f"Error loading YOLO model: {e}")
                print("Please run: pip uninstall torch torchvision -y && pip install torch==2.6.0 torchvision==0.21.0")
                self.model_loaded = False
        else:
            self.model_loaded = False

    def detect_phone_usage(self, frame, person_boxes, phone_boxes):
        """Check if person is using phone based on proximity and overlap"""
        phone_users = []

        for person_box in person_boxes:
            px1, py1, px2, py2 = person_box
            person_center_x = (px1 + px2) / 2
            person_center_y = (py1 + py2) / 2
            person_width = px2 - px1
            person_height = py2 - py1

            for phone_box in phone_boxes:
                phx1, phy1, phx2, phy2 = phone_box
                phone_center_x = (phx1 + phx2) / 2
                phone_center_y = (phy1 + phy2) / 2

                # Check if phone is within person's bounding box
                phone_in_person = (phx1 >= px1 and phx2 <= px2 and phy1 >= py1 and phy2 <= py2)

                # Check if phone overlaps with upper body (top 60% of person box)
                upper_body_limit = py1 + (person_height * 0.6)
                phone_in_upper_body = (phy1 < upper_body_limit and phy2 < upper_body_limit)

                # Check horizontal proximity (phone within person's width range)
                horizontal_proximity = abs(phone_center_x - person_center_x) < (person_width * 0.5)

                # Person is using phone if any condition is met
                if phone_in_person or (phone_in_upper_body and horizontal_proximity):
                    phone_users.append({
                        'person_box': person_box,
                        'phone_box': phone_box,
                        'using_phone': True
                    })
                    break

        return phone_users

    def process_frame(self, frame):
        """Process single frame with all detections"""
        results = {
            'persons': [],
            'phones': [],
            'phone_users': []
        }

        if not self.model_loaded:
            return results

        # YOLO detection
        yolo_results = self.yolo_model(frame, verbose=False)

        person_boxes = []
        phone_boxes = []

        for result in yolo_results:
            boxes = result.boxes
            for box in boxes:
                cls = int(box.cls[0])
                conf = float(box.conf[0])
                class_name = self.yolo_model.names[cls]

                if conf > 0.5:  # Confidence threshold
                    x1, y1, x2, y2 = map(int, box.xyxy[0])

                    if class_name == 'person':
                        person_boxes.append([x1, y1, x2, y2])
                        results['persons'].append({
                            'box': [x1, y1, x2, y2],
                            'confidence': conf
                        })
                    elif class_name == 'cell phone':
                        phone_boxes.append([x1, y1, x2, y2])
                        results['phones'].append({
                            'box': [x1, y1, x2, y2],
                            'confidence': conf
                        })

        # Detect phone usage
        if person_boxes and phone_boxes:
            results['phone_users'] = self.detect_phone_usage(frame, person_boxes, phone_boxes)

        return results

    def draw_detections(self, frame, results):
        """Draw all detections on frame"""
        annotated_frame = frame.copy()

        # Draw persons
        for person in results['persons']:
            x1, y1, x2, y2 = person['box']
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(annotated_frame, f"Person {person['confidence']:.2f}",
                       (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Draw phones
        for phone in results['phones']:
            x1, y1, x2, y2 = phone['box']
            cv2.rectangle(annotated_frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
            cv2.putText(annotated_frame, f"Phone {phone['confidence']:.2f}",
                       (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

        # Draw phone users with highlight
        for user in results['phone_users']:
            px1, py1, px2, py2 = user['person_box']
            cv2.rectangle(annotated_frame, (px1, py1), (px2, py2), (0, 255, 255), 3)
            cv2.putText(annotated_frame, "USING PHONE",
                       (px1, py1-30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

        # Add stats
        stats_text = f"Persons: {len(results['persons'])} | Phones: {len(results['phones'])} | Using Phone: {len(results['phone_users'])}"
        cv2.putText(annotated_frame, stats_text,
                   (10, frame.shape[0]-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        return annotated_frame

    def save_detection_to_db(self, frame, results):
        """Save detection image and data to Django database"""
        # Generate filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"phone_detection_{timestamp}.jpg"

        # Encode frame to jpg
        _, buffer = cv2.imencode('.jpg', frame)
        image_content = ContentFile(buffer.tobytes(), name=filename)

        # Create database entry
        detection = PhoneUsageDetection(
            person_count=len(results['persons']),
            phone_count=len(results['phones']),
            phone_users_count=len(results['phone_users']),
            description=f"Detected {len(results['phone_users'])} person(s) using phone"
        )
        detection.image.save(filename, image_content, save=True)

        print(f"✓ Saved detection to database: {filename}")
        return detection

    def run_webcam(self, save_interval=3):
        """Run detection on webcam feed and save to database"""

        if not self.model_loaded:
            print("\n" + "="*60)
            print("ERROR: YOLO model not loaded!")
            print("="*60)
            print("\nPlease fix the torch/torchvision compatibility:")
            print("1. pip uninstall torch torchvision -y")
            print("2. pip install torch==2.6.0 torchvision==0.21.0")
            print("3. Run this script again")
            print("="*60)
            return

        cap = cv2.VideoCapture(0)

        print("=" * 60)
        print("Starting Django Multi-Detection System")
        print("=" * 60)
        print(f"✓ Auto-save interval: {save_interval} seconds")
        print("✓ Detection: Person + Phone Usage")
        print("✓ Press 'q' to quit")
        print("✓ Press 's' to manually save current frame")
        print("=" * 60)

        frame_count = 0
        last_save_time = datetime.now()
        detection_active = False

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Cannot read from webcam")
                break

            frame_count += 1

            # Process frame
            results = self.process_frame(frame)

            # Draw detections
            annotated_frame = self.draw_detections(frame, results)

            # Add live status indicator
            status_color = (0, 255, 0) if results['phone_users'] else (100, 100, 100)
            cv2.circle(annotated_frame, (20, 20), 8, status_color, -1)
            cv2.putText(annotated_frame, "LIVE", (35, 25),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, status_color, 2)

            # Display
            cv2.imshow('Phone Detection System - LIVE', annotated_frame)

            # Auto-save if phone users detected and interval passed
            if results['phone_users']:
                current_time = datetime.now()
                time_diff = (current_time - last_save_time).total_seconds()

                if time_diff >= save_interval:
                    self.save_detection_to_db(annotated_frame, results)
                    last_save_time = current_time

                    print(f"\n{'='*60}")
                    print(f"⚠️  ALERT: {len(results['phone_users'])} person(s) using phone!")
                    print(f"   Persons detected: {len(results['persons'])}")
                    print(f"   Phones detected: {len(results['phones'])}")
                    print(f"   Time: {current_time.strftime('%H:%M:%S')}")
                    print(f"{'='*60}\n")

                    detection_active = True
            else:
                if detection_active:
                    print("✓ No phone usage detected - monitoring...")
                    detection_active = False

            # Handle key presses
            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                print("\nShutting down detection system...")
                break
            elif key == ord('s'):
                # Manual save
                self.save_detection_to_db(annotated_frame, results)
                print(f"✓ Manual save triggered - Frame #{frame_count}")

        cap.release()
        cv2.destroyAllWindows()
        print(f"\n✓ Detection system stopped. Total frames processed: {frame_count}")


if __name__ == "__main__":
    detector = DjangoMultiDetectionSystem()

    # Run on webcam (saves detection every 3 seconds when phone usage detected)
    detector.run_webcam(save_interval=3)
