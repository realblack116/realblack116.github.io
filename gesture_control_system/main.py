pyimport sys
from PySide6.QtWidgets import QApplication
from gui.main_window import GestureControlSystem

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GestureControlSystem()
    window.show()
    sys.exit(app.exec())
