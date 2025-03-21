from PySide6.QtWidgets import QMainWindow, QTabWidget, QMessageBox
from PySide6.QtGui import QPixmap, QAction
from core.gesture_recognition import GestureRecognitionThread
from core.actions import GestureActions
from gui.tabs.main_tab import MainTab
from gui.tabs.training_tab import TrainingTab
from gui.tabs.mapping_tab import MappingTab
from gui.tabs.settings_tab import SettingsTab
from utils.logger import Logger
import os
import json
import datetime

class GestureControlSystem(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("제스처 인식 컴퓨터 제어 시스템")
        self.setGeometry(100, 100, 1000, 600)
        self.logger = Logger()
        self.gesture_thread = GestureRecognitionThread(self)
        self.gesture_thread.updateFrame.connect(self.update_frame)
        self.gesture_thread.gestureDetected.connect(self.handle_gesture)
        self.gesture_thread.updateTrainingProgress.connect(self.update_training_progress)
        self.actions = GestureActions(self)
        self.gesture_actions = {
            "Up": self.actions.action_volume_up,
            "Down": self.actions.action_volume_down,
            "Left": self.actions.action_previous,
            "Right": self.actions.action_next
        }
        self.tabs = QTabWidget()
        self.setup_menu()
        self.main_tab = MainTab(self, self.gesture_thread)
        self.training_tab = TrainingTab(self, self.gesture_thread)
        self.mapping_tab = MappingTab(self, self.gesture_thread)
        self.settings_tab = SettingsTab(self, self.gesture_thread)
        self.tabs.addTab(self.main_tab, "메인")
        self.tabs.addTab(self.training_tab, "제스처 학습")
        self.tabs.addTab(self.mapping_tab, "제스처 매핑")
        self.tabs.addTab(self.settings_tab, "설정")
        self.setCentralWidget(self.tabs)
        self.logger.set_text_widget(self.main_tab.status_text)
        self.load_settings()
    
    def setup_menu(self):
        menubar = self.menuBar()
        file_menu = menubar.addMenu("파일")
        save_action = QAction("설정 저장", self)
        save_action.triggered.connect(self.save_settings)
        file_menu.addAction(save_action)
        load_action = QAction("설정 불러오기", self)
        load_action.triggered.connect(self.load_settings)
        file_menu.addAction(load_action)
        exit_action = QAction("종료", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        help_menu = menubar.addMenu("도움말")
        about_action = QAction("정보", self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def save_settings(self):
        settings = {
            "min_area": self.settings_tab.min_area_slider.value(),
            "threshold": self.settings_tab.threshold_slider.value(),
            "cooldown": self.settings_tab.cooldown_spin.value(),
            "max_frames": self.settings_tab.max_frames_spin.value(),
            "mirroring": self.settings_tab.mirroring_checkbox.isChecked()
        }
        try:
            settings_path = os.path.join(self.gesture_thread.output_path, "settings.json")
            with open(settings_path, 'w') as f:
                json.dump(settings, f, indent=4)
            self.log_status("설정이 저장되었습니다.")
            QMessageBox.information(self, "저장 성공", "설정이 저장되었습니다.")
        except Exception as e:
            QMessageBox.critical(self, "저장 실패", f"설정 저장 실패: {str(e)}")
    
    def load_settings(self):
        settings_path = os.path.join(self.gesture_thread.output_path, "settings.json")
        if os.path.exists(settings_path):
            try:
                with open(settings_path, 'r') as f:
                    settings = json.load(f)
                self.settings_tab.apply_settings_from_dict(settings)
                self.log_status("설정이 로드되었습니다.")
            except Exception as e:
                self.log_status(f"설정 로드 실패: {str(e)}")
        self.mapping_tab.load_mappings()
    
    def update_frame(self, image):
        self.main_tab.video_label.setPixmap(QPixmap.fromImage(image))
    
    def handle_gesture(self, gesture):
        self.main_tab.last_gesture_label.setText(f"마지막 인식: {gesture}")
        self.log_status(f"제스처 인식: {gesture}")
        if gesture in self.mapping_tab.mapping_combos:
            action_text = self.mapping_tab.mapping_combos[gesture].currentText()
            self.execute_action(action_text)
    
    def execute_action(self, action_text):
        if action_text == "볼륨 증가":
            self.actions.action_volume_up()
        elif action_text == "볼륨 감소":
            self.actions.action_volume_down()
        elif action_text == "이전":
            self.actions.action_previous()
        elif action_text == "다음":
            self.actions.action_next()
        elif action_text == "재생/일시정지":
            self.actions.action_play_pause()
        elif action_text == "스크롤 업":
            self.actions.action_scroll_up()
        elif action_text == "스크롤 다운":
            self.actions.action_scroll_down()
    
    def update_training_progress(self, current, total):
        self.training_tab.update_progress(current, total)
    
    def log_status(self, message):
        self.logger.log(message)
    
    def show_about(self):
        QMessageBox.about(
            self, 
            "제스처 인식 컴퓨터 제어 시스템",
            "제스처 인식 컴퓨터 제어 시스템 v1.0\n\n"
            "이 애플리케이션은 OpenCV와 PySide6를 사용하여 웹캠을 통해 "
            "손동작 제스처를 인식하고 이를 통해 컴퓨터를 제어할 수 있는 시스템입니다.\n\n"
            "사용자는 자신만의 제스처를 학습시켜 다양한 컴퓨터 작업을 "
            "편리하게 제어할 수 있습니다."
        )
    
    def closeEvent(self, event):
        if self.gesture_thread.isRunning():
            self.gesture_thread.status = False
            self.gesture_thread.wait()
        event.accept()
