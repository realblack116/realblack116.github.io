import datetime

class Logger:
    def __init__(self, text_widget=None):
        self.text_widget = text_widget
    
    def set_text_widget(self, text_widget):
        self.text_widget = text_widget
    
    def log(self, message):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message}"
        print(formatted_message)
        if self.text_widget:
            self.text_widget.append(formatted_message)
            scrollbar = self.text_widget.verticalScrollBar()
            scrollbar.setValue(scrollbar.maximum())
        return formatted_message
