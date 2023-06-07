import socket
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QDialog, QFileDialog
from PyQt5.uic import loadUi 
from PyQt5.QtGui import *
import sys
IP = socket.gethostbyname(socket.gethostname())
PORT = 4411
ADDR = (socket.gethostbyname("MAIN-PC-BUTTER"), 4455)
ADDR = None
NAME = ""
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
        global IP, PORT, NAME
        try:
            self.hostName = self.hostTextBox.text()
            self.PortNumber = int(self.PostTextBox.text())
            self.name = self.NameTextBox.text()
        except ValueError:
            print("Invalid port number!")
        
        IP = socket.gethostbyname(self.hostName)
        PORT = self.PortNumber
        NAME = self.name
        if self.test_server_connection():
            widget.setCurrentIndex(widget.currentIndex()+1)
        else:
            #Change Label that connection failed
            print("Failed")
    def test_server_connection(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as test_socket:
                test_socket.settimeout(5)  # Set a timeout for the connection attempt
                test_socket.connect((socket.gethostbyname(self.hostName), self.PortNumber))
                return True  # Connection successful
        except (socket.timeout, ConnectionRefusedError):
            return False  # Connection failed or timed out

class clientControl(QDialog):
    IP = ""
    PortNumber = 1
    name = "Butter"

    def __init__(self):
        super(clientControl,self).__init__()
        loadUi("ClientControl.ui",self)
        self.sendButton.clicked.connect(self.sendMessage)
        self.BrowseButton.clicked.connect(self.browsefiles)
        global IP, PORT, NAME
        self.IP = IP
        self.PortNumber = PORT
        self.name = NAME
    def sendMessage(self):
        global IP, PORT
        print(f'Sending Message: {IP}, {PORT}')

    def sendFile(self):
        #Connecting to server
        if self.filename != "Attachment" and self.browse_textbox.text() != "Attachment":
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.connect((self.IP, self.PortNumber))
            with open(self.filename, "rb") as file:
                data = file.read()

            client.send(self.filename.encode(FORMAT))
            msg = client.recv(SIZE).decode(FORMAT)
            print(f"[SERVER]: {msg}")
            client.sendall(data)
            msg = client.recv(SIZE).decode(FORMAT)
            print(f"[SERVER]: {msg}")

            client.close()
            self.browse_textbox.setText("Attachment")
            print("Sending File")




    def browsefiles(self):
        file_filter = "Audio Files (*.mp3 *.wav);;Image Files (*.png *.jpg *.jpeg);;Text Files (*.txt);;Word Documents (*.docx)"
        self.filename, _ = QFileDialog.getOpenFileName(self, 'Open File', '', file_filter)
        if self.filename:
            self.browse_textbox.setText(self.filename)


def main(ADDR):
    print(socket.gethostname())
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
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
    widget = QtWidgets.QStackedWidget()
    clientStart = clientStartUp()
    clientControlVar = clientControl()
    widget.addWidget(clientStart)
    widget.addWidget(clientControlVar)
    widget.show()
    IP = socket.gethostbyname(clientStart.hostName)
    PORT = clientStart.PortNumber
    ADDR = (IP, PORT)
    print(ADDR)

    

    sys.exit(app.exec_())