import cv2
from vision import VisionModule


vision = VisionModule()

camera = cv2.VideoCapture(0)

while True:

    success, frame = camera.read()

    if not success:
        break

    frame, count, attendance = vision.detect_faces(
        frame
    )

    cv2.putText(
        frame,
        f"Faces: {count}",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2
    )

    y_position = 80

    for student, status in attendance.items():

        cv2.putText(
            frame,
            f"{student}: {status}",
            (20, y_position),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (255, 0, 0),
            2
        )

        y_position += 30

    cv2.imshow(
        "Attendance System",
        frame
    )

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()