import cv2
from ultralytics import YOLO

print("Testing YOLO detection...")

# Load model
print("Loading YOLOv8 model...")
model = YOLO('yolov8n.pt')
print("✓ Model loaded successfully")

# Test with webcam
print("\nTesting webcam detection...")
print("Press 'q' to quit")

cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ERROR: Cannot open webcam")
    exit()

frame_count = 0
while True:
    ret, frame = cap.read()
    if not ret:
        print("ERROR: Cannot read frame")
        break

    frame_count += 1

    # Run detection
    results = model(frame, verbose=False)

    # Draw results
    annotated_frame = results[0].plot()

    # Show detections
    cv2.putText(annotated_frame, f"Frame: {frame_count}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow('YOLO Test', annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
print(f"\n✓ Test completed. Processed {frame_count} frames")
