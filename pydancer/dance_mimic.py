import cv2
import numpy as np
import time
import pygame
from mediapipe.python.solutions import pose as mp_pose


# well, i wanted to do more python cool stuffs
# currently i went on tiktok and i see avideo where by they ses python to do some  

pose = mp_pose.Pose(
    static_image_mode=False,
    model_complexity=0, 
    enable_segmentation=False,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

video_path = "jackiechan.mp4"
audio_path = "jackiechan.mp3"

# video_path = "peller.mp4"
# audio_path = "peller.mp3"

# video_path = "yu.mp4"
# audio_path = "yu.mp3"

# video_path = "dance.mp4"
# audio_path = "dance.mp3"
cap = cv2.VideoCapture(video_path)

fps = cap.get(cv2.CAP_PROP_FPS)
WIDTH, HEIGHT = 337, 600

pygame.mixer.init()
pygame.mixer.music.load(audio_path)

def draw_stick_figure(canvas_shape, landmarks):
    canvas = np.zeros(canvas_shape, dtype=np.uint8)

    def p(idx):
        lm = landmarks[idx]
        return int(lm.x * WIDTH), int(lm.y * HEIGHT)

    try:
        joints = {
            "head": p(mp_pose.PoseLandmark.NOSE),
            "ls": p(mp_pose.PoseLandmark.LEFT_SHOULDER),
            "rs": p(mp_pose.PoseLandmark.RIGHT_SHOULDER),
            "le": p(mp_pose.PoseLandmark.LEFT_ELBOW),
            "re": p(mp_pose.PoseLandmark.RIGHT_ELBOW),
            "lw": p(mp_pose.PoseLandmark.LEFT_WRIST),
            "rw": p(mp_pose.PoseLandmark.RIGHT_WRIST),
            "lh": p(mp_pose.PoseLandmark.LEFT_HIP),
            "rh": p(mp_pose.PoseLandmark.RIGHT_HIP),
            "lk": p(mp_pose.PoseLandmark.LEFT_KNEE),
            "rk": p(mp_pose.PoseLandmark.RIGHT_KNEE),
            "la": p(mp_pose.PoseLandmark.LEFT_ANKLE),
            "ra": p(mp_pose.PoseLandmark.RIGHT_ANKLE),
        }

        bones = [
            ("head", "ls"), ("head", "rs"), ("ls", "rs"), ("lh", "rh"),
            ("ls", "le"), ("le", "lw"),
            ("rs", "re"), ("re", "rw"),
            ("ls", "lh"), ("rs", "rh"),
            ("lh", "lk"), ("lk", "la"),
            ("rh", "rk"), ("rk", "ra")
        ]

        for a, b in bones:
            cv2.line(canvas, joints[a], joints[b], (0, 255, 255), 3)

        for point in joints.values():
            cv2.circle(canvas, point, 5, (255, 255, 255), -1)
    except:
        pass

    return canvas

pygame.mixer.music.play()
start_time = time.time()

while cap.isOpened():
    elapsed_ms = pygame.mixer.music.get_pos()
    
    if elapsed_ms == -1:
        elapsed_ms = (time.time() - start_time) * 1000
    
    target_frame = int((elapsed_ms / 1000.0) * fps)
    current_frame = int(cap.get(cv2.CAP_PROP_POS_FRAMES))

    while current_frame < target_frame:
        ret, frame = cap.read()
        if not ret: break
        current_frame += 1
    
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (WIDTH, HEIGHT))
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)

    stick = np.zeros_like(frame)
    if results.pose_landmarks:
        stick = draw_stick_figure(frame.shape, results.pose_landmarks.landmark)

    combined = np.hstack((frame, stick))

    cv2.putText(combined, f"FPS: {fps:.1f} (Sync Active)", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow("Dance vs Python (With Sound)", combined)

    key = cv2.waitKey(1) & 0xFF
    if key == 27 or key == ord('q'):
        break

cap.release()
pygame.mixer.music.stop()
cv2.destroyAllWindows()
