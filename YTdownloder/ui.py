import os
import re
import threading
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QLineEdit, QPushButton, QRadioButton, QFileDialog, 
                            QProgressBar, QMessageBox, QButtonGroup)
from PyQt5.QtCore import Qt, pyqtSlot
from downloader import DownloadWorker

class YouTubeDownloaderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("YouTube 다운로더")
        self.setGeometry(100, 100, 550, 420)
        self.setStyleSheet("background-color: #f0f0f0;")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)
        self.main_layout.setContentsMargins(20, 20, 20, 20)
        self.init_ui()
        self.download_thread = None
        self.worker = None
    
    def init_ui(self):
        url_label = QLabel("YouTube URL:")
        url_label.setStyleSheet("font: 12pt Arial;")
        self.url_entry = QLineEdit()
        self.url_entry.setStyleSheet("font: 12pt Arial; padding: 5px;")
        self.main_layout.addWidget(url_label)
        self.main_layout.addWidget(self.url_entry)
        self.main_layout.addSpacing(15)
        path_layout = QHBoxLayout()
        path_label = QLabel("저장 경로:")
        path_label.setStyleSheet("font: 12pt Arial;")
        self.path_entry = QLineEdit(os.path.join(os.path.expanduser("~"), "Downloads"))
        self.path_entry.setStyleSheet("font: 12pt Arial; padding: 5px;")
        self.browse_button = QPushButton("찾아보기")
        self.browse_button.setStyleSheet("font: 10pt Arial;")
        self.browse_button.clicked.connect(self.browse_path)
        path_layout.addWidget(path_label)
        path_layout.addWidget(self.path_entry)
        path_layout.addWidget(self.browse_button)
        self.main_layout.addLayout(path_layout)
        self.main_layout.addSpacing(15)
        options_layout = QHBoxLayout()
        format_label = QLabel("형식:")
        format_label.setStyleSheet("font: 12pt Arial;")
        self.format_group = QButtonGroup(self)
        self.video_radio = QRadioButton("비디오 (mp4)")
        self.video_radio.setStyleSheet("font: 11pt Arial;")
        self.video_radio.setChecked(True)
        self.audio_radio = QRadioButton("오디오 (mp3)")
        self.audio_radio.setStyleSheet("font: 11pt Arial;")
        self.format_group.addButton(self.video_radio, 1)
        self.format_group.addButton(self.audio_radio, 2)
        options_layout.addWidget(format_label)
        options_layout.addWidget(self.video_radio)
        options_layout.addWidget(self.audio_radio)
        options_layout.addStretch()
        self.main_layout.addLayout(options_layout)
        self.main_layout.addSpacing(15)
        quality_layout = QHBoxLayout()
        quality_label = QLabel("품질:")
        quality_label.setStyleSheet("font: 12pt Arial;")
        self.quality_group = QButtonGroup(self)
        self.high_radio = QRadioButton("고품질")
        self.high_radio.setStyleSheet("font: 11pt Arial;")
        self.high_radio.setChecked(True)
        self.medium_radio = QRadioButton("중간")
        self.medium_radio.setStyleSheet("font: 11pt Arial;")
        self.low_radio = QRadioButton("저품질")
        self.low_radio.setStyleSheet("font: 11pt Arial;")
        self.quality_group.addButton(self.high_radio, 1)
        self.quality_group.addButton(self.medium_radio, 2)
        self.quality_group.addButton(self.low_radio, 3)
        quality_layout.addWidget(quality_label)
        quality_layout.addWidget(self.high_radio)
        quality_layout.addWidget(self.medium_radio)
        quality_layout.addWidget(self.low_radio)
        quality_layout.addStretch()
        self.main_layout.addLayout(quality_layout)
        self.main_layout.addSpacing(15)
        self.filename_label = QLabel("")
        self.filename_label.setStyleSheet("font: 10pt Arial;")
        self.main_layout.addWidget(self.filename_label)
        status_layout = QHBoxLayout()
        self.progress_label = QLabel("대기 중")
        self.progress_label.setStyleSheet("font: 10pt Arial;")
        self.speed_label = QLabel("")
        self.speed_label.setStyleSheet("font: 10pt Arial;")
        self.speed_label.setAlignment(Qt.AlignRight)
        status_layout.addWidget(self.progress_label)
        status_layout.addWidget(self.speed_label)
        self.main_layout.addLayout(status_layout)
        self.progressbar = QProgressBar()
        self.progressbar.setStyleSheet("""
            QProgressBar {
                border: 1px solid #bbb;
                border-radius: 3px;
                text-align: center;
                height: 20px;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
            }
        """)
        self.main_layout.addWidget(self.progressbar)
        self.main_layout.addSpacing(15)
        button_layout = QHBoxLayout()
        self.download_button = QPushButton("다운로드")
        self.download_button.setStyleSheet("""
            font: bold 12pt Arial; 
            color: white; 
            background-color: #4CAF50;
            border: none;
            padding: 8px;
            border-radius: 4px;
        """)
        self.download_button.clicked.connect(self.start_download)
        self.cancel_button = QPushButton("취소")
        self.cancel_button.setStyleSheet("""
            font: bold 12pt Arial; 
            color: white; 
            background-color: #f44336;
            border: none;
            padding: 8px;
            border-radius: 4px;
        """)
        self.cancel_button.clicked.connect(self.cancel_download)
        self.cancel_button.setEnabled(False)
        button_layout.addWidget(self.download_button)
        button_layout.addWidget(self.cancel_button)
        self.main_layout.addLayout(button_layout)
        self.main_layout.addStretch()
        self.copyright_label = QLabel("© 2025 Lim Dong Kwan. All Rights Reserved.")
        self.copyright_label.setStyleSheet("font: 8pt Arial; color: #666666;")
        self.copyright_label.setAlignment(Qt.AlignCenter)
        self.main_layout.addWidget(self.copyright_label)
    
    def browse_path(self):
        directory = QFileDialog.getExistingDirectory(self, "저장 경로 선택")
        if directory:
            self.path_entry.setText(directory)
    
    def is_valid_youtube_url(self, url):
        youtube_regex = r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/(watch\?v=|embed/|v/|.+\?v=)?([^&=%\?]{11})'
        return re.match(youtube_regex, url) is not None
    
    def start_download(self):
        url = self.url_entry.text().strip()
        if not url:
            QMessageBox.critical(self, "오류", "YouTube URL을 입력해주세요.")
            return
        if not self.is_valid_youtube_url(url):
            reply = QMessageBox.question(self, "경고", "유효한 YouTube URL이 아닌 것 같습니다. 그래도 시도할까요?",
                                      QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return
        save_path = self.path_entry.text()
        if not os.path.exists(save_path):
            try:
                os.makedirs(save_path)
            except:
                QMessageBox.critical(self, "오류", "저장 경로를 생성할 수 없습니다.")
                return
        format_type = "audio" if self.audio_radio.isChecked() else "video"
        quality = "high"
        if self.medium_radio.isChecked():
            quality = "medium"
        elif self.low_radio.isChecked():
            quality = "low"
        self.progressbar.setValue(0)
        self.progress_label.setText("다운로드 준비 중...")
        self.speed_label.setText("")
        self.filename_label.setText("")
        self.download_button.setEnabled(False)
        self.cancel_button.setEnabled(True)
        self.worker = DownloadWorker()
        self.worker.progress_changed.connect(self.update_progress)
        self.worker.status_changed.connect(self.update_status)
        self.worker.speed_changed.connect(self.update_speed)
        self.worker.filename_changed.connect(self.update_filename)
        self.worker.download_complete.connect(self.download_finished)
        self.download_thread = threading.Thread(
            target=self.worker.download, 
            args=(url, save_path, format_type, quality)
        )
        self.download_thread.daemon = True
        self.download_thread.start()
    
    def cancel_download(self):
        if self.worker:
            self.worker.cancel()
    
    @pyqtSlot(float)
    def update_progress(self, value):
        self.progressbar.setValue(int(value))
    
    @pyqtSlot(str)
    def update_status(self, text):
        self.progress_label.setText(text)
    
    @pyqtSlot(str)
    def update_speed(self, text):
        self.speed_label.setText(text)
    
    @pyqtSlot(str)
    def update_filename(self, text):
        self.filename_label.setText(text)
    
    @pyqtSlot(bool, str)
    def download_finished(self, success, message):
        self.download_button.setEnabled(True)
        self.cancel_button.setEnabled(False)
        if success:
            QMessageBox.information(self, "성공", f"다운로드가 완료되었습니다!\n파일: {message}")
        else:
            QMessageBox.critical(self, "오류", f"다운로드 중 오류가 발생했습니다:\n{message}")