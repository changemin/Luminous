import numpy as np
from imutils import face_utils
import cv2
import time
import dlib

from tensorflow.keras.models import load_model


class EyeDetector:
    def __init__(self, predictor_path):
        # dlib이라는 라이브러리의 얼굴 인식 모듈(detector)을 초기화하고,
        # 얼굴의 특징적 부분(눈썹, 귀, 눈 등, "랜드마크"라고 부름)을 인식하는 predictor 생성
        print("[INFO] 안면 특징부 인식기 로딩 중...")
        self.detector = dlib.get_frontal_face_detector()
        self.predictor = dlib.shape_predictor(predictor_path)

        # 왼쪽 눈, 오른쪽 눈에 해당하는 랜드마크의 시작과 끝 인덱스를 가져옴
        (self.left_start_idx,
         self.left_end_idx) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (self.right_start_idx,
         self.right_end_idx) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

        self.IMG_SIZE = (24, 24)

        self.model = load_model('train/model.h5')
        self.model.summary()

        # 비디오 스트르밍 시작
        print("[INFO] 비디오 스트림 쓰레드 시작 중..")
        print("[INFO] q를 눌러 중지하세요.")

    def update(self, frame):
        # 현재 프레임을 가져오고, 흑백 사진으로 전환
        # (RGB 세 값을 사용하는게 아닌 한 픽셀당 한 값이기 때문에 처리가 더 쉽다)
        # frame = imutils.resize(frame, width=450)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        open_probability = None
        left_eye_rect = None
        right_eye_rect = None

        # detector 함수를 통해 가져온 프레임에서 얼굴 인식하여 (1개 이상) 가져옴
        face_rects = self.detector(gray, 0)

        # 가져온 얼굴들 중에서 크기가 가장 큰 얼굴만 추출
        if len(list(face_rects)) > 0:
            face_rect = max(face_rects, key=lambda rect: rect.area())

            # 얼굴 영역에서 랜드마크 가져오고, 배열 형태로 변환
            landmark_shapes = self.predictor(gray, face_rect)
            landmark_shapes = face_utils.shape_to_np(landmark_shapes)

            # 좌측과 우측 눈의 좌표를 가져오고, 이를 사용하여 눈의 크기 계산
            left_eye_img, left_eye_rect = crop_eye(
                gray, landmark_shapes[self.left_start_idx:self.left_end_idx])
            right_eye_img, right_eye_rect = crop_eye(
                gray, landmark_shapes[self.right_start_idx:self.right_end_idx])

            left_eye_img = cv2.resize(left_eye_img, dsize=self.IMG_SIZE)
            right_eye_img = cv2.resize(right_eye_img, dsize=self.IMG_SIZE)

            left_eye_input = left_eye_img.copy().reshape(
                (1, self.IMG_SIZE[0], self.IMG_SIZE[1], 1)).astype(np.float32) / 255.
            right_eye_input = right_eye_img.copy().reshape(
                (1, self.IMG_SIZE[0], self.IMG_SIZE[1], 1)).astype(np.float32) / 255.

            left_pred = self.model.predict(left_eye_input)
            right_pred = self.model.predict(right_eye_input)

            open_probability = (left_pred + right_pred) / 2.0
            print(open_probability)

        return (left_eye_rect, right_eye_rect, open_probability)


def crop_eye(img, eye_points):
    x1, y1 = np.amin(eye_points, axis=0)
    x2, y2 = np.amax(eye_points, axis=0)
    cx, cy = (x1 + x2) / 2, (y1 + y2) / 2

    w = (x2 - x1) * 1.2
    h = w

    margin_x, margin_y = w / 2, h / 2

    min_x, min_y = int(cx - margin_x), int(cy - margin_y)
    max_x, max_y = int(cx + margin_x), int(cy + margin_y)

    eye_rect = np.rint([min_x, min_y, max_x, max_y]).astype(np.int)

    eye_img = img[eye_rect[1]:eye_rect[3], eye_rect[0]:eye_rect[2]]

    return eye_img, eye_rect
