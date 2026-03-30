import cv2
import os
import numpy as np
import pickle
from django.conf import settings

def train_model():
    faces = []
    labels = []
    label_map = {}
    label_id = 0

    base_dir = os.path.join(settings.MEDIA_ROOT, 'faces')

    for person in os.listdir(base_dir):
        person_path = os.path.join(base_dir, person)
        label_map[label_id] = person

        for img in os.listdir(person_path):
            img_path = os.path.join(person_path, img)
            face = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
            faces.append(face)
            labels.append(label_id)

        label_id += 1

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.train(faces, np.array(labels))
    recognizer.save('face_model.yml')

    with open('labels.pkl', 'wb') as f:
        pickle.dump(label_map, f)