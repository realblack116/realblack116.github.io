from PySide6.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QLabel, 
                              QGroupBox, QComboBox, QPushButton, QMessageBox)
import os
import json

class MappingTab(QWidget):
    def __init__(self, parent, gesture_thread):
        super().__init__()
        self.parent = parent
        self.gesture_thread = gesture_thread
        self.mapping_combos = {}
        self.setup_ui()
    
    def setup_ui(self):
        layout = QVBoxLayout()
        instruction_label = QLabel("제스처와 수행할 액션을 매핑하세요.")
        layout.addWidget(instruction_label)
        self.mapping_group = QGroupBox("제스처 매핑")
        self.mapping_layout = QGridLayout()
        self.mapping_layout.addWidget(QLabel("제스처"), 0, 0)
        self.mapping_layout.addWidget(QLabel("액션"), 0, 1)
        row = 1
        for gesture in ["Up", "Down", "Left", "Right"]:
            self.mapping_layout.addWidget(QLabel(gesture), row, 0)
            action_combo = QComboBox()
            for action in ["볼륨 증가", "볼륨 감소", "이전", "다음", "재생/일시정지", "스크롤 업", "스크롤 다운"]:
                action_combo.addItem(action)
            if gesture == "Up":
                action_combo.setCurrentText("볼륨 증가")
            elif gesture == "Down":
                action_combo.setCurrentText("볼륨 감소")
            elif gesture == "Left":
                action_combo.setCurrentText("이전")
            elif gesture == "Right":
                action_combo.setCurrentText("다음")
            self.mapping_combos[gesture] = action_combo
            self.mapping_layout.addWidget(action_combo, row, 1)
            row += 1
        self.update_gesture_mappings()
        self.mapping_group.setLayout(self.mapping_layout)
        layout.addWidget(self.mapping_group)
        save_button = QPushButton("매핑 저장")
        save_button.clicked.connect(self.save_mappings)
        layout.addWidget(save_button)
        self.setLayout(layout)
    
    def update_gesture_mappings(self):
        row_count = 5
        for i in range(self.mapping_layout.count()-1, -1, -1):
            item = self.mapping_layout.itemAt(i)
            if item and item.widget():
                if isinstance(item.widget(), QLabel) or isinstance(item.widget(), QComboBox):
                    row_pos, col_pos, _, _ = self.mapping_layout.getItemPosition(i)
                    if row_pos >= row_count:
                        self.mapping_layout.removeItem(item)
                        item.widget().deleteLater()
        for gesture_name in self.gesture_thread.gestures_db.keys():
            if gesture_name in ["Up", "Down", "Left", "Right"]:
                continue
            self.mapping_layout.addWidget(QLabel(gesture_name), row_count, 0)
            action_combo = QComboBox()
            for action in ["볼륨 증가", "볼륨 감소", "이전", "다음", "재생/일시정지", "스크롤 업", "스크롤 다운"]:
                action_combo.addItem(action)
            self.mapping_combos[gesture_name] = action_combo
            self.mapping_layout.addWidget(action_combo, row_count, 1)
            row_count += 1
    
    def save_mappings(self):
        mappings = {}
        for gesture, combo in self.mapping_combos.items():
            mappings[gesture] = combo.currentText()
        try:
            mappings_path = os.path.join(self.gesture_thread.output_path, "mappings.json")
            with open(mappings_path, 'w') as f:
                json.dump(mappings, f, indent=4)
            self.parent.log_status("제스처 매핑이 저장되었습니다.")
            QMessageBox.information(self, "저장 성공", "제스처 매핑이 저장되었습니다.")
        except Exception as e:
            QMessageBox.critical(self, "저장 실패", f"매핑 저장 실패: {str(e)}")
    
    def load_mappings(self):
        mappings_path = os.path.join(self.gesture_thread.output_path, "mappings.json")
        if not os.path.exists(mappings_path):
            return
        try:
            with open(mappings_path, 'r') as f:
                mappings = json.load(f)
            for gesture, action in mappings.items():
                if gesture in self.mapping_combos:
                    index = self.mapping_combos[gesture].findText(action)
                    if index >= 0:
                        self.mapping_combos[gesture].setCurrentIndex(index)
            self.parent.log_status("제스처 매핑이 로드되었습니다.")
        except Exception as e:
            self.parent.log_status(f"매핑 로드 실패: {str(e)}")
