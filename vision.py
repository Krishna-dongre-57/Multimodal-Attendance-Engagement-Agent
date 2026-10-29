import cv2
import mediapipe as mp


class VisionModule:

    def __init__(self):

        self.mp_face_detection = mp.solutions.face_detection

        self.face_detector = self.mp_face_detection.FaceDetection(
            model_selection=0,
            min_detection_confidence=0.6
        )

        self.attendance = {}

    def detect_faces(self, frame):

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        results = self.face_detector.process(
            rgb_frame
        )

        face_count = 0

        if results.detections:

            face_count = len(results.detections)

            for idx, detection in enumerate(results.detections):

                student_id = f"Student_{idx+1}"

                self.attendance[student_id] = "Present"

                bbox = detection.location_data.relative_bounding_box

                h, w, _ = frame.shape

                x = int(bbox.xmin * w)
                y = int(bbox.ymin * h)
                width = int(bbox.width * w)
                height = int(bbox.height * h)

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + width, y + height),
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    student_id,
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

        return frame, face_count, self.attendance