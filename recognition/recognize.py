import cv2
import pickle
import requests
import time

# --- CONFIGURATION ---
ESP_IP = "http://192.168.1.100" # TODO: Update with your ESP8266 IP (e.g., http://192.168.4.1)
THINGSPEAK_API_KEY = "0R1DI0GVVU0HE64M"
THINGSPEAK_INTERVAL = 16.0      # 15s limit for free tier
CONFIDENCE_THRESHOLD = 50       # Lower is better (0 = perfect match)
REQUEST_INTERVAL = 2.0          # Seconds between requests to avoid flooding
# ---------------------

def recognize_face():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('face_model.yml')

    with open('labels.pkl', 'rb') as f:
        labels = pickle.load(f)

    cam = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    )
    
    last_esp_request_time = 0
    last_thingspeak_time = 0

    print("Starting Face Recognition...")
    print(f"Confidence Threshold: {CONFIDENCE_THRESHOLD}")
    print(f"Target ESP8266: {ESP_IP}")

    while True:
        ret, frame = cam.read()
        if not ret:
            print("Failed to grab frame")
            break
            
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:
            face = gray[y:y+h, x:x+w]
            label_id, confidence = recognizer.predict(face)
            
            # Check Authorization
            if confidence < CONFIDENCE_THRESHOLD:
                name = labels[label_id]
                status_text = f"Authorized: {name}"
                color = (0, 255, 0) # Green
                cmd_endpoint = "/1"
            else:
                name = "Unknown"
                status_text = "Unauthorized"
                color = (0, 0, 255) # Red
                cmd_endpoint = "/0"

            # Draw UI
            cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
            cv2.putText(frame, f"{name} ({int(confidence)})", (x,y-10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            cv2.putText(frame, status_text, (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.8, color, 2)
            
            # Send Command to ESP8266 (Rate Limited)
            current_time = time.time()
            if current_time - last_esp_request_time > REQUEST_INTERVAL:
                try:
                    url = f"{ESP_IP}{cmd_endpoint}"
                    print(f"Sending to ESP (also logging to cloud): {url} ...")
                    requests.get(url, timeout=0.5) 
                except Exception as e:
                    print(f"ESP Error: {e}")
                
                last_esp_request_time = current_time

            # Log to ThingSpeak (Rate Limited separately)
            if current_time - last_thingspeak_time > THINGSPEAK_INTERVAL:
                try:
                    val = 1 if cmd_endpoint == "/1" else 0
                    ts_url = f"http://api.thingspeak.com/update?api_key={THINGSPEAK_API_KEY}&field1={val}"
                    print(f"Logging to ThingSpeak: {val} ...")
                    requests.get(ts_url, timeout=1.0)
                except Exception as e:
                    print(f"ThingSpeak Error: {e}")
                
                last_thingspeak_time = current_time

        cv2.imshow("Live Recognition", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'): # 'q' to exit
            break
        if cv2.waitKey(1) == 27: # ESC to exit
            break

    cam.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    recognize_face()