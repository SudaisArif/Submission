import cv2
import mediapipe as mp
import threading

mpHands = mp.solutions.hands
mpDrawing = mp.solutions.drawing_utils

class HandGestureRecognition:
    def __init__(self, onSpidermanDetect, onGunDetect, onRelease):
        self.running = True
        self.onSpidermanDetect = onSpidermanDetect  
        self.onGunDetect = onGunDetect              
        self.onRelease = onRelease                 
        self.cap = cv2.VideoCapture(0)
        self.currentGesture = None  # Track the current detected gesture

        # Start a thread for gesture detection
        threading.Thread(target=self._detectGestureInBackground, daemon=True).start()

    def _detectGestureInBackground(self):
        with mpHands.Hands(min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
            while self.running:
                ret, frame = self.cap.read()
                if not ret:
                    continue

                frameRgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = hands.process(frameRgb)

                detectedGesture = None
                if results.multi_hand_landmarks:
                    for handLandmarks in results.multi_hand_landmarks:
                        landmarks = handLandmarks.landmark

                        # Check for gestures
                        if isSpidermanSymbol(landmarks):
                            detectedGesture = "spiderman"
                        elif isGunFingerSymbol(landmarks):
                            detectedGesture = "gun"

                        # Draw landmarks
                        mpDrawing.draw_landmarks(frame, handLandmarks, mpHands.HAND_CONNECTIONS)

                # Handle gesture detection
                if detectedGesture:
                    if detectedGesture != self.currentGesture:
                        if detectedGesture == "spiderman":
                            self.onSpidermanDetect()
                        elif detectedGesture == "gun":
                            self.onGunDetect()
                        self.currentGesture = detectedGesture
                else:
                    if self.currentGesture is not None:
                        self.onRelease()
                        self.currentGesture = None

                # Display the frame
                cv2.imshow('Hand Tracking', frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    self.stop()

    def stop(self):
        self.running = False
        self.cap.release()
        cv2.destroyAllWindows()


def isSpidermanSymbol(landmarks):
    # Detects the Spiderman hand symbol.
    thumbUp = landmarks[4].y < landmarks[3].y
    indexUp = landmarks[8].y < landmarks[6].y
    middleDown = landmarks[12].y > landmarks[10].y
    ringDown = landmarks[16].y > landmarks[14].y
    pinkyUp = landmarks[20].y < landmarks[18].y

    return thumbUp and indexUp and middleDown and ringDown and pinkyUp


def isGunFingerSymbol(landmarks):
    # Detects the Gun Finger hand symbol.
    thumbUp = landmarks[4].y < landmarks[3].y
    indexUp = landmarks[8].y < landmarks[6].y
    middleUp = landmarks[12].y < landmarks[10].y
    ringDown = landmarks[16].y > landmarks[14].y
    pinkyDown = landmarks[20].y > landmarks[18].y

    return thumbUp and indexUp and middleUp and ringDown and pinkyDown
