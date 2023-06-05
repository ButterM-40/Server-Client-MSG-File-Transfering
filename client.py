import socket
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog
from PyQt5.uic import loadUi 
from PyQt5.QtGui import *
import sys
IP = socket.gethostbyname(socket.gethostname())
PORT = 4455
ADDR = (socket.gethostbyname("MAIN-PC-BUTTER"), 4455)
FORMAT = "utf-8"
SIZE = 1024

class clientStartUp(QDialog):
    hostName = ""
    PortNumber = 1
    name = "Butter"

    def __init__(self):
        super(clientStartUp,self).__init__()
        loadUi("clientStartUp.ui",self)
        self.connectButton.clicked.connect(self.connectToServer)
    def connectToServer(self):
        self.hostName = self.hostTextBox.toPlainText()
        self.PortNumber = int(self.PostTextBox.toPlainText())
        self.name = self.NameTextBox.toPlainText()
        ADDR = (socket.gethostbyname(self.hostName), self.PortNumber)
        main()
def main():
    print(socket.gethostname())
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ADDR = (socket.gethostbyname("MAIN-PC-BUTTER"), 4455)
    client.connect(ADDR)
    file = open("data/Transfer.txt", "r")
    data = file.read()

    
    client.send("Transfer.txt".encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")
    client.send(data.encode(FORMAT))
    msg = client.recv(SIZE).decode(FORMAT)
    print(f"[SERVER]: {msg}")

    file.close()
    client.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget=QtWidgets.QStackedWidget()
    clientStart = clientStartUp()
    widget.addWidget(clientStart)
    widget.show()
    IP = socket.gethostbyname(clientStart.hostName)
    PORT = clientStart.PortNumber
    ADDR = (IP, PORT)
    print(ADDR)

    

    sys.exit(app.exec_())