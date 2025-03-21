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
    updateTrainingProgress = Signal(int, int)
    
    def __init__(self, parent=None):
        QThread.__init__(self, parent)
        self.status = True
        self.cap = None
        
        self.hand_cascade_file = os.path.join(cv2.data.haarcascades, "haarcascade_frontalface_default.xml")
        
        self.min_area = 3000
        self.threshold = 40
        
        self.mode = "detection"
        self.recording_gesture = False
        self.current_gesture_name = ""
        self.recorded_frames = []
        self.max_recording_frames = 30
        self.recording_count = 0
        )
        self.is_mirroring = True
        
        self.output_path = "gesture_data"
        Path(self.output_path).mkdir(exist_ok=True)
        
        self.gestures_db = {}
        self.load_gestures_database()
        
        self.prev_frame = None
        self.movement_history = []
        
        self.last_gesture = None
        self.gesture_cooldown = 20
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
            
            if self.is_mirroring:
                frame = cv2.flip(frame, 1)
            
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray_frame = cv2.GaussianBlur(gray_frame, (21, 21), 0)
            gray_frame = cv2.equalizeHist(gray_frame)
            
            if self.prev_frame is None:
                self.prev_frame = gray_frame
                continue
            
            frame_delta = cv2.absdiff(self.prev_frame, gray_frame)
            thresh = cv2.threshold(frame_delta, self.threshold, 255, cv2.THRESH_BINARY)[1]
            
            thresh = cv2.dilate(thresh, None, iterations=2)
            contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            movement_detected = False
            movement_vector = (0, 0)
            
            for contour in contours:
                if cv2.contourArea(contour) < self.min_area:
                    continue
                
                movement_detected = True
                (x, y, w, h) = cv2.boundingRect(contour)
                
                center_x = x + w//2
                center_y = y + h//2
                
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.circle(frame, (center_x, center_y), 5, (0, 0, 255), -1)
                
                if self.movement_history:
                    prev_x, prev_y = self.movement_history[-1]
                    dx = center_x - prev_x
                    dy = center_y - prev_y
                    movement_vector = (dx, dy)
                    
                    cv2.arrowedLine(frame, (prev_x, prev_y), (center_x, center_y),
                                   (255, 0, 0), 2, tipLength=0.3)
                
                self.movement_history.append((center_x, center_y))
                if len(self.movement_history) > 15:  # 10에서 15로 늘려 더 긴 패턴 기억
                    self.movement_history.pop(0)
            
            if self.mode == "training" and self.recording_gesture:
                if movement_detected:
                    self.recorded_frames.append({
                        "movement_vector": movement_vector,
                        "movement_history": self.movement_history.copy() if self.movement_history else [],
                        "contour_area": [cv2.contourArea(c) for c in contours if cv2.contourArea(c) >= self.min_area]
                    })
                    self.recording_count += 1
                    
                    self.updateTrainingProgress.emit(self.recording_count, self.max_recording_frames)
                    
                    if self.recording_count >= self.max_recording_frames:
                        self.stop_gesture_recording()
                
                cv2.putText(frame, f"Recording: {self.current_gesture_name}", (10, 30),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.putText(frame, f"Frames: {self.recording_count}/{self.max_recording_frames}", (10, 60),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            elif self.mode == "detection":
                if self.cooldown_counter > 0:
                    self.cooldown_counter -= 1
                
                if movement_detected and len(self.movement_history) >= 5 and self.cooldown_counter == 0:
                    gesture = self.detect_gesture()
                    if gesture:
                        if (not self.last_gesture or 
                            gesture != self.last_gesture or 
                            self.cooldown_counter >= 30):
                            self.last_gesture = gesture
                            self.gestureDetected.emit(gesture)
                            self.cooldown_counter = self.gesture_cooldown
                            
                            cv2.putText(frame, f"Detected: {gesture}", (10, 30),
                                      cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            
            self.prev_frame = gray_frame
            
            mirror_status = "미러링: 켜짐" if self.is_mirroring else "미러링: 꺼짐"
            cv2.putText(frame, mirror_status, (frame.shape[1] - 150, 30), 
                      cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            
            color_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = color_frame.shape
            img = QImage(color_frame.data, w, h, ch * w, QImage.Format.Format_RGB888)
            scaled_img = img.scaled(640, 480, Qt.AspectRatioMode.KeepAspectRatio)
            
            self.updateFrame.emit(scaled_img)
            
        if self.cap:
            self.cap.release()
    
    def detect_gesture(self):
        """기본적인 제스처 인식 구현"""
        if len(self.movement_history) < 3:
            return None
        
        start_x, start_y = self.movement_history[0]
        end_x, end_y = self.movement_history[-1]
        
        dx = end_x - start_x
        dy = end_y - start_y
        
        magnitude = (dx**2 + dy**2)**0.5
        if magnitude < 35:  # 50에서 35로 감소
            return None
        
        if self.gestures_db:
            return self.match_with_trained_gestures(dx, dy, magnitude)
        
        return self.detect_basic_gesture(dx, dy)
    
    def match_with_trained_gestures(self, dx, dy, magnitude):
        """향상된 제스처 매칭 알고리즘"""
        best_match = None
        best_score = float('inf')
        
        for gesture_name, gesture_data in self.gestures_db.items():
            if "frames" not in gesture_data or not gesture_data["frames"]:
                continue
            
            scores = []
            for frame in gesture_data["frames"]:
                if "movement_history" not in frame or not frame["movement_history"]:
                    continue
                
                g_start_x, g_start_y = frame["movement_history"][0]
                g_end_x, g_end_y = frame["movement_history"][-1]
                
                g_dx = g_end_x - g_start_x
                g_dy = g_end_y - g_start_y
                g_magnitude = (g_dx**2 + g_dy**2)**0.5
                
                if g_magnitude == 0:
                    continue
                
                n_dx, n_dy = dx/magnitude, dy/magnitude
                n_g_dx, n_g_dy = g_dx/g_magnitude, g_dy/g_magnitude
                
                similarity = 1 - ((n_dx*n_g_dx + n_dy*n_g_dy) + 1) / 2
                scores.append(similarity)
            
            score = min(scores) if scores else float('inf')
            
            if score < best_score and score < 0.45:  # 0.3에서 0.45로 증가
                best_score = score
                best_match = gesture_name
        
        return best_match if best_match else self.detect_basic_gesture(dx, dy)
    
    def detect_basic_gesture(self, dx, dy):
        """개선된 기본 방향 제스처 인식"""
        angle = np.degrees(np.arctan2(dy, dx))
        
        if -45 <= angle <= 45:
            return "Right"
        elif 45 < angle <= 135:
            return "Down"
        elif -135 <= angle < -45:
            return "Up"
        else:  # 나머지 각도 (-180~-135 및 135~180)
            return "Left"
