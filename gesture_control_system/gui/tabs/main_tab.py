from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QLabel, 
                              QGroupBox, QTextEdit, QPushButton)
from PySide6.QtGui import QPixmap

class MainTab(QWidget):
    def __init__(self, parent, gesture_thread):
        super().__init__()
        self.parent = parent
        self.gesture_thread = gesture_thread
        self.setup_ui()
    
    def setup_ui(self):
        layout = QHBoxLayout()
        
        self.video_label = QLabel()
        self.video_label.setMinimumSize(640, 480)
        self.video_label.setStyleSheet("border: 1px solid #cccccc;")
        
        controls_layout = QVBoxLayout()
        
        status_group = QGroupBox("상태")
        status_layout = QVBoxLayout()
        
        self.status_text = QTextEdit()
        self.status_text.setReadOnly(True)
        self.status_text.setMaximumHeight(200)
        status_layout.addWidget(self.status_text)
        
        status_group.setLayout(status_layout)
        controls_layout.addWidget(status_group)
        
        control_group = QGroupBox("제어")
        control_layout = QVBoxLayout()
        
        self.start_button = QPushButton("시작")
        self.start_button.clicked.connect(self.start_detection)
        control_layout.addWidget(self.start_button)
        
        self.stop_button = QPushButton("중지")
        self.stop_button.clicked.connect(self.stop_detection)
        self.stop_button.setEnabled(False)
        control_layout.addWidget(self.stop_button)
        
        control_group.setLayout(control_layout)
        controls_layout.addWidget(control_group)
        
        gestures_group = QGroupBox("인식된 제스처")
        gestures_layout = QVBoxLayout()
        
        self.last_gesture_label = QLabel("마지막 인식: 없음")
        gestures_layout.addWidget(self.last_gesture_label)
        
        gestures_group.setLayout(gestures_layout)
        controls_layout.addWidget(gestures_group)
        
        controls_layout.addStretch(1)
        
        layout.addWidget(self.video_label, 2)
        layout.addLayout(controls_layout, 1)
        
        self.setLayout(layout)
    
    def start_detection(self):
        if not self.gesture_thread.isRunning():
            self.gesture_thread.status = True
            self.gesture_thread.start()
            
            self.start_button.setEnabled(False)
            self.stop_button.setEnabled(True)
            
            mode = "학습" if self.gesture_thread.mode == "training" else "감지"
            self.parent.log_status(f"제스처 {mode}를 시작합니다.")
    
    def stop_detection(self):
        if self.gesture_thread.isRunning():
            self.gesture_thread.status = False
            
            self.start_button.setEnabled(True)
            self.stop_button.setEnabled(False)
            
            if self.gesture_thread.mode == "training" and self.gesture_thread.recording_gesture:
                self.gesture_thread.stop_gesture_recording()
            
            self.parent.log_status("제스처 인식이 중지되었습니다.")
