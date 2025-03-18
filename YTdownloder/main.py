import sys
from PyQt5.QtWidgets import QApplication
from ui import YouTubeDownloaderApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = YouTubeDownloaderApp()
    window.show()
    sys.exit(app.exec_())
