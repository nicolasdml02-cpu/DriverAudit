import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import DriverPulseWindow

def main():
    app = QApplication(sys.argv)
    janela = DriverPulseWindow()
    janela.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()