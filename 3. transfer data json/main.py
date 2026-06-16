# FIX #2 & #3: QtWebEngine.initialize() HARUS dipanggil paling pertama,
# sebelum QApplication dibuat. AA_UseDesktopOpenGL dihapus karena
# konflik dengan WebEngine di GPU yang berbeda.
import sys

from PyQt5.QtWebEngine import QtWebEngine
QtWebEngine.initialize()  # ← WAJIB paling pertama

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtQml import *
from PyQt5.QtWidgets import *
from PyQt5.QtQuick import *
from PyQt5.QtWebEngineWidgets import QWebEngineView
import json
import os
import csv
import io



sensor2 = 898

# FIX: Hanya AA_EnableHighDpiScaling yang aman lintas-PC.
# AA_UseDesktopOpenGL DIHAPUS → penyebab crash 0xC0000005 di GPU lain.
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)


# --- BACKEND KHUSUS UNTUK JEMBATAN KE JAVASCRIPT ---
class Backend(QObject):

    thetaChanged = pyqtSignal(float)

    def __init__(self):
        super().__init__()
        self._theta = 130.0

    @pyqtProperty(float, notify=thetaChanged)
    def theta(self):
        return self._theta

    

    @pyqtSlot(str)
    def pop(self, msg):
        print(msg)




    @pyqtSlot(result=str)
    def getPositionData(self):

        try:
            with open("position.json", "r") as f:
                data = json.load(f)

            return json.dumps({
                "x": data.get("x", 0),
                "y": data.get("y", 0),
                "z": data.get("z", 0),
                "theta": data.get("theta", 0)
            })

        except FileNotFoundError:
            return json.dumps({
                "x": 0,
                "y": 0,
                "z": 0,
                "theta": 0,
                "status": "no_file"
            })

        except Exception as e:
            return json.dumps({
                "x": 0,
                "y": 0,
                "z": 0,
                "theta": 0,
                "error": str(e)
            })
        
        
backend: Backend = None



class table(QObject):
    def __init__(self):
        super().__init__()
        self.app = QApplication(sys.argv)

        global ship_backend
        backend = Backend()

        self.engine = QQmlApplicationEngine()
        self.engine.rootContext().setContextProperty("Backend", backend)
        self.engine.load(QUrl.fromLocalFile("main.qml"))

        sys.exit(self.app.exec_())


if __name__ == "__main__":


    main = table()
