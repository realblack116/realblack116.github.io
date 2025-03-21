from PySide6.QtCore import QThread, Signal, Qt
from PySide6.QtGui import QImage
import cv2
import numpy as np
import os
import json
import datetime
from pathlib import Path


class GestureRecognitionThread(QThread):
    updateFrame = Signal(QImage)
    gestureDetected = Signal(str)
    updateTrainingProgress = Signal(int, int)  # current, total
    
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.status = True
        self.cap = None
        
        # 손 감지를 위한 기본 Haar cascade 파일
        self.hand_cascade_file = os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml")
        
        # 제스처 감지 매개변수 - 더 민감하게 조정
        self.min_area = 3000  # 5000에서 3000으로 감소 (더 작은 움직임도 감지)
        self.threshold = 40   # 70에서 40으로 감소 (더 미세한 변화도 감지)
        
        # 제스처 모드 설정
        self.mode = "detection"  # "detection" 또는 "training"
        self.recording_gesture = False
        self.current_gesture_name = ""
        self.recorded_frames = []
        self.max_recording_frames = 30
        self.recording_count = 0
        
        # 미러링 설정 (기본값: 활성화)
        self.is_mirroring = True
        
        # 출력 디렉토리 생성
        self.output_path = "gesture_data"
        Path(self.output_path).mkdir(exist_ok=True)
        
        # 제스처 데이터베이스
        self.gestures_db = {}
        self.load_gestures_database()
        
        # 움직임 감지 변수
        self.prev_frame = None
        self.movement_history = []
        
        # 제스처 인식 변수
        self.last_gesture = None
        self.gesture_cooldown = 20  # 프레임 단위 쿨다운
        self.cooldown_counter = 0
    
    def set_mode(self, mode):
        self.mode = mode
    
    def set_mirroring(self, enabled):
        """미러링 모드 설정"""
        self.is_mirroring = enabled
        
    def start_gesture_recording(self, gesture_name):
        self.current_gesture_name = gesture_name
        self.recording_gesture = True
        self.recorded_frames = []
        self.recording_count = 0
        
    def stop_gesture_recording(self):
        if self.recording_gesture and self.recorded_frames:
            # 제스처 데이터 저장
            self.gestures_db[self.current_gesture_name] = {
                "frames": self.recorded_frames,
                "timestamp": datetime.datetime.now().isoformat(),
                "frame_count": len(self.recorded_frames)
            }
            self.save_gestures_database()
            
        self.recording_gesture = False
        self.current_gesture_name = ""
        self.recorded_frames = []
    
    def load_gestures_database(self):
        db_path = os.path.join(self.output_path, "gestures_db.json")
        if os.path.exists(db_path):
            try:
                with open(db_path, 'r') as f:
                    self.gestures_db = json.load(f)
            except Exception as e:
                print(f"Error loading gestures database: {e}")
                self.gestures_db = {}
    
    def save_gestures_database(self):
        db_path = os.path.join(self.output_path, "gestures_db.json")
        try:
            with open(db_path, 'w') as f:
                json.dump(self.gestures_db, f, indent=4)
        except Exception as e:
            print(f"Error saving gestures database: {e}")
    
    def run(self):
        self.cap = cv2.VideoCapture(0)
        
        while self.status:
            ret, frame = self.cap.read()
            if not ret:
                continue
            
            # 미러링 - 사용자 설정에 따라 적용
            if self.is_mirroring:
                frame = cv2.flip(frame, 1)
            
            # 프레임 그레이스케일 변환 
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # 더 효과적인 노이즈 제거
            gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)
            # 대비 향상 추가
            gray_frame = cv2.equalizeHist(gray_frame)
            
            # 움직임 감지
            if self.prev_frame is None:
                self.prev_frame = gray_frame
                continue
            
            # 프레임 간 차이 계산
            frame_delta = cv2.absdiff(self.prev_frame, gray_frame)
            thresh = cv2.threshold(frame_delta, self.threshold, 255, cv2.THRESH_BINARY)[1]
            
            # 노이즈 제거 및 윤곽 개선
            thresh = cv2.dilate(thresh, None, iterations=2)
            contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # 큰 동작만 처리
            movement_detected = False
            movement_vector = (0, 0)
            
            for contour in contours:
                if cv2.contourArea(contour) < self.min_area:
                    continue
                
                movement_detected = True
                (x, y, w, h) = cv2.boundingRect(contour)
                
                # 움직임 중심점
                center_x = x + w//2
                center_y = y + h//2
                
                # 윤곽 표시
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)
                
                # 이동 벡터 계산
                if self.movement_history:
                    prev_x, prev_y = self.movement_history[-1]
                    dx = center_x - prev_x
                    dy = center_y - prev_y
                    movement_vector = (dx, dy)
                    
                    # 움직임 방향 표시
                    cv2.arrowedLine(frame, (prev_x, prev_y), (center_x, center_y),
                                   (255, 0, 0), 2, tipLength=0.3)
                
                # 이동 이력 업데이트
                self.movement_history.append((center_x, center_y))
                if len(self.movement_history) > 15:  # 10에서 15로 늘려 더 긴 패턴 기억
                    self.movement_history.pop(0)
            
            # 트레이닝 모드인 경우
            if self.mode == "training" and self.recording_gesture:
                if movement_detected:
                    # 움직임 데이터 저장
                    self.recorded_frames.append({
                        "movement_vector": movement_vector,
                        "movement_history": self.movement_history.copy() if self.movement_history else [],
                        "contour_area": [cv2.contourArea(c) for c in contours if cv2.contourArea(c) >= self.min_area]
                    })
                    self.recording_count += 1
                    
                    # 진행 상황 업데이트
                    self.updateTrainingProgress.emit(self.recording_count, self.max_recording_frames)
                    
                    # 최대 프레임 수 도달시 녹화 중지
                    if self.recording_count >= self.max_recording_frames:
                        self.stop_gesture_recording()
                
                # 녹화 중임을 표시
                cv2.putText(frame, f"Recording: {self.current_gesture_name}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.putText(frame, f"Frames: {self.recording_count}/{self.max_recording_frames}", (10, 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            # 감지 모드인 경우
            elif self.mode == "detection":
                # 쿨다운 감소
                if self.cooldown_counter > 0:
                    self.cooldown_counter -= 1
                
                # 제스처 인식 - 더 안정적인 감지를 위해 수정
                if movement_detected and len(self.movement_history) >= 5 and self.cooldown_counter == 0:
                    # 최소 5개의 이동 포인트가 있어야 함
                    gesture = self.detect_gesture()
                    if gesture:
                        # 이전 제스처와 같더라도 일정 시간(30프레임) 이후에는 다시 신호 보냄
                        if (not self.last_gesture or 
                            gesture != self.last_gesture or 
                            self.cooldown_counter >= 30):
                            self.last_gesture = gesture
                            self.gestureDetected.emit(gesture)
                            self.cooldown_counter = self.gesture_cooldown
                            
                            # 제스처 이름 표시
                            cv2.putText(frame, f"Detected: {gesture}", (10, 30),
                                      cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            # 현재 프레임 저장
            self.prev_frame = gray_frame
            
            # 미러링 상태 표시
            mirror_status = "미러링: 켜짐" if self.is_mirroring else "미러링: 꺼짐"
            cv2.putText(frame, mirror_status, (frame.shape[1] - 150, 30), 
                      cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            # 화면 표시용 이미지 변환
            color_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = color_frame.shape
            img = QImage(color_frame.data, w, h, ch * w, QImage.Format.Format_RGB888)
            scaled_img = img.scaled(640, 480, Qt.AspectRatioMode.KeepAspectRatio)
            
            # 이미지 업데이트 시그널 전송
            self.updateFrame.emit(scaled_img)
            
        if self.cap:
            self.cap.release()
    
    def detect_gesture(self):
        """기본적인 제스처 인식 구현"""
        # 움직임 방향 분석
        if len(self.movement_history) < 3:
            return None
        
        # 처음과 마지막 포인트 사이의 움직임 분석
        start_x, start_y = self.movement_history[0]
        end_x, end_y = self.movement_history[-1]
        
        dx = end_x - start_x
        dy = end_y - start_y
        
        # 움직임의 크기 계산
        magnitude = (dx**2 + dy**2)**0.5
        if magnitude < 35:  # 50에서 35로 감소
            return None
        
        # 학습된 제스처가 있는 경우, 매칭 시도
        if self.gestures_db:
            return self.match_with_trained_gestures(dx, dy, magnitude)
        
        # 기본 방향 제스처 인식
        return self.detect_basic_gesture(dx, dy)
    
    def match_with_trained_gestures(self, dx, dy, magnitude):
        """향상된 제스처 매칭 알고리즘"""
        best_match = None
        best_score = float('inf')
        
        # 각 제스처와 비교
        for gesture_name, gesture_data in self.gestures_db.items():
            if "frames" not in gesture_data or not gesture_data["frames"]:
                continue
            
            # 점수 계산 방식 개선
            scores = []
            for frame in gesture_data["frames"]:
                if "movement_history" not in frame or not frame["movement_history"]:
                    continue
                
                # 학습된 제스처의 처음과 마지막 포인트
                g_start_x, g_start_y = frame["movement_history"][0]
                g_end_x, g_end_y = frame["movement_history"][-1]
                
                g_dx = g_end_x - g_start_x
                g_dy = g_end_y - g_start_y
                g_magnitude = (g_dx**2 + g_dy**2)**0.5
                
                if g_magnitude == 0:
                    continue
                
                # 방향 벡터 정규화
                n_dx, n_dy = dx/magnitude, dy/magnitude
                n_g_dx, n_g_dy = g_dx/g_magnitude, g_dy/g_magnitude
                
                # 코사인 유사도 계산 (1 - 코사인 유사도 = 거리)
                similarity = 1 - ((n_dx*n_g_dx + n_dy*n_g_dy) + 1) / 2
                scores.append(similarity)
            
            # 가장 좋은 매칭 점수 사용 (평균 대신) - 더 관대한 매칭
            score = min(scores) if scores else float('inf')
            
            # 매칭 임계값 증가 (더 관대하게)
            if score < best_score and score < 0.45:  # 0.3에서 0.45로 증가
                best_score = score
                best_match = gesture_name
        
        return best_match if best_match else self.detect_basic_gesture(dx, dy)
    
    def detect_basic_gesture(self, dx, dy):
        """개선된 기본 방향 제스처 인식"""
        # 각도 기반 제스처 인식 (더 정확)
        angle = np.degrees(np.arctan2(dy, dx))
        
        # 각도를 기반으로 방향 결정
        if -45 <= angle <= 45:
            return "Right"
        elif 45 < angle <= 135:
            return "Down"
        elif -135 <= angle < -45:
            return "Up"
        else:  # 나머지 각도 (-180~-135 및 135~180)
            return "Left"