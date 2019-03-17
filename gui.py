import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox, QDesktopWidget, QGridLayout
from PyQt5.QtGui import QIcon
 
class App(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):                
        self.resize(450, 250)
        self.center()  
        self.setWindowTitle('Yellow Page Scrapper')    
        title = QLabel('Input Search Item: ')
        titleEdit = QLineEdit()
        grid = QGridLayout()
        grid.setSpacing(2)
        grid.addWidget(title, 1, 0)
        grid.addWidget(titleEdit, 1, 1)
        self.setLayout(grid) 
        self.show()


    def center(self):    
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        

    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Message',
            "Are you sure to quit?", QMessageBox.Yes | 
            QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()        
               
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())