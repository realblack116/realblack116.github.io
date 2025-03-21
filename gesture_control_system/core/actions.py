import pyautogui
import datetime

class GestureActions:
    def __init__(self, parent=None):
        self.parent = parent
    
    def action_volume_up(self):
        pyautogui.press('volumeup')
        if self.parent and hasattr(self.parent, 'log_status'):
            self.parent.log_status("액션 실행: 볼륨 증가")
    
    def action_volume_down(self):
        pyautogui.press('volumedown')
        if self.parent and hasattr(self.parent, 'log_status'):
            self.parent.log_status("액션 실행: 볼륨 감소")
    
    def action_previous(self):
        pyautogui.press('prevtrack')
        if self.parent and hasattr(self.parent, 'log_status'):
            self.parent.log_status("액션 실행: 이전 트랙")
    
    def action_next(self):
        pyautogui.press('nexttrack')
        if self.parent and hasattr(self.parent, 'log_status'):
            self.parent.log_status("액션 실행: 다음 트랙")
    
    def action_play_pause(self):
        pyautogui.press('playpause')
        if self.parent and hasattr(self.parent, 'log_status'):
            self.parent.log_status("액션 실행: 재생/일시정지")
    
    def action_scroll_up(self):
        pyautogui.scroll(10)
        if self.parent and hasattr(self.parent, 'log_status'):
            self.parent.log_status("액션 실행: 스크롤 업")
    
    def action_scroll_down(self):
        pyautogui.scroll(-10)
        if self.parent and hasattr(self.parent, 'log_status'):
            self.parent.log_status("액션 실행: 스크롤 다운")
