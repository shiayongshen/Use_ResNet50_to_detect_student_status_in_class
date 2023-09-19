import cv2
import datetime

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow('frame', frame)

    if cv2.waitKey(1) == ord(' '):
        now = datetime.datetime.now()
        filename = f"{now.strftime('%Y%m%d_%H%M%S')}.jpg"
        face_img = gray[y:y + h, x:x + w]
        face_img_resized = cv2.resize(face_img, (224, 224))
        cv2.imwrite(filename, face_img_resized)
        print(f"Saved image as {filename}")

    if cv2.waitKey(1) == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()