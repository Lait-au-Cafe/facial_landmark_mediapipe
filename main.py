import socket
import json
import cv2
import mediapipe as mp

mp_face_mesh = mp.solutions.face_mesh

HOST = "localhost"
PORT = 50007

camera_id = 1

cap = cv2.VideoCapture(camera_id)
with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
  with mp_face_mesh.FaceMesh(
      max_num_faces=1,
      refine_landmarks=True,
      min_detection_confidence=0.5,
      min_tracking_confidence=0.5) as face_mesh:
    while cap.isOpened():
      success, image = cap.read()
      if not success:
        print("Ignoring empty camera frame.")
        continue

      # To improve performance, optionally mark the image as not writeable to
      # pass by reference.
      image.flags.writeable = False
      image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
      results = face_mesh.process(image)

      if results.multi_face_landmarks:
        landmark = []
        for l in results.multi_face_landmarks[0].landmark:
          landmark.append({
            'x': l.x, 
            'y': l.y, 
            'z': l.z, 
          })
        sock.sendto(json.dumps(landmark).encode('utf-8'), (HOST, PORT))

  cap.release()