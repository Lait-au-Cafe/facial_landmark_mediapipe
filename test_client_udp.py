import socket
import json
import numpy as np
import cv2

HOST = "localhost"
PORT = 50007

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
  sock.bind((HOST, PORT))

  while True:
    try:
      msg, addr = sock.recvfrom(65535)
      landmark = json.loads(msg.decode('utf-8'))
      display = np.zeros((512, 512, 3))
      for pt in landmark:
        print(f"x: {pt['x']}, y: {pt['y']}, type={type(pt['x'])}")
        x = int(pt['x']*512)
        y = int(pt['y']*512)
        cv2.circle(display, center=(x, y), radius=2, color=(0, 255, 0), thickness=1)
      cv2.imshow("Facial Landmarks", display)
      if cv2.waitKey(5) & 0xFF == 27: break
    except KeyboardInterrupt:
      print("Quit. ")
      break
            