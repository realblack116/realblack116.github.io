```python
import os
import yt_dlp
from PyQt5.QtCore import QObject, pyqtSignal

class DownloadWorker(QObject):
    progress_changed = pyqtSignal(float)
    status_changed = pyqtSignal(str)
    speed_changed = pyqtSignal(str)
    filename_changed = pyqtSignal(str)
    download_complete = pyqtSignal(bool, str)
    
    def __init__(self):
        super().__init__()
        self.is_cancelled = False
        self.ydl = None
        self.current_file = ""
    
    def progress_hook(self, d):
        if self.is_cancelled:
            raise Exception("다운로드가 취소되었습니다.")
            
        if d['status'] == 'downloading':
            filename = d.get('filename', '').split('/')[-1].split('\\')[-1]
            if filename:
                self.current_file = filename
                self.filename_changed.emit(f"파일: {filename}")
            
            percent_str = d.get('_percent_str', '?%').strip()
            try:
                percent = float(percent_str.replace('%', ''))
                self.progress_changed.emit(percent)
            except:
                self.progress_changed.emit(0)
            
            speed = d.get('_speed_str', '알 수 없음')
            eta = d.get('_eta_str', '')
            speed_info = f"속도: {speed}"
            if eta:
                speed_info += f" (남은 시간: {eta})"
            self.speed_changed.emit(speed_info)
            
            self.status_changed.emit(f"다운로드 중... {percent_str}")
            
        elif d['status'] == 'finished':
            self.status_changed.emit("다운로드 완료, 처리 중...")
            self.progress_changed.emit(100)
            
        elif d['status'] == 'error':
            self.status_changed.emit("다운로드 오류 발생")

    def download(self, url, save_path, format_type, quality):
        try:
            video_quality = {
                'high': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'medium': 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[height<=720][ext=mp4]/best[height<=720]',
                'low': 'bestvideo[height<=480][ext=mp4]+bestaudio[ext=m4a]/best[height<=480][ext=mp4]/best[height<=480]'
            }
            
            audio_quality = {
                'high': '192',
                'medium': '128',
                'low': '96'
            }
            
            if format_type == "audio":
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': audio_quality[quality],
                    }],
                    'progress_hooks': [self.progress_hook],
                }
            else:
                ydl_opts = {
                    'format': video_quality[quality],
                    'outtmpl': os.path.join(save_path, '%(title)s.%(ext)s'),
                    'progress_hooks': [self.progress_hook],
                }
            
            with yt_dlp.YoutubeDL(ydl_opts) as self.ydl:
                self.status_changed.emit("정보 가져오는 중...")
                info = self.ydl.extract_info(url, download=not self.is_cancelled)
                
                if info and not self.is_cancelled:
                    title = info.get('title', '알 수 없는 제목')
                    self.status_changed.emit(f"다운로드 완료: {title}")
                    self.download_complete.emit(True, self.current_file)
                    
        except Exception as e:
            self.status_changed.emit(f"오류 발생: {str(e)}")
            self.download_complete.emit(False, str(e))
    
    def cancel(self):
        self.is_cancelled = True
        self.status_changed.emit("다운로드 취소 중...")
        
        if self.ydl:
            try:
                self.ydl.interrupt()
            except:
                pass
```
