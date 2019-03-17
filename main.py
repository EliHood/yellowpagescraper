from functools import partial
from PyQt5 import QtCore, QtGui, QtWidgets

class ScrapyWorker(QtCore.QObject):
    logChanged = QtCore.pyqtSignal(str)
    started = QtCore.pyqtSignal()
    finished = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super(ScrapyWorker, self).__init__(parent)
        self._process = QtCore.QProcess(self)
        self._process.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        self._process.readyReadStandardOutput.connect(self.on_readyReadStandardOutput)
        self._process.setProgram('scrapy')
        self._process.started.connect(self.started)
        self._process.finished.connect(self.finished)

    def run(self, project, spider):
        self._process.setWorkingDirectory(project)
        self._process.setArguments(['crawl', spider])
        self._process.start()

    @QtCore.pyqtSlot()
    def on_readyReadStandardOutput(self):
        data = self._process.readAllStandardOutput().data().decode()
        self.logChanged.emit(data)

    @QtCore.pyqtSlot()
    def stop(self):
        self._process.kill()

    def spiders(self, project):
        process = QtCore.QProcess()
        process.setProcessChannelMode(QtCore.QProcess.MergedChannels)
        process.setWorkingDirectory(project)
        loop = QtCore.QEventLoop()
        process.finished.connect(loop.quit)
        process.start('scrapy', ['list'])
        loop.exec_()
        return process.readAllStandardOutput().data().decode().split()

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.project_le = QtWidgets.QLineEdit()
        self.project_button = QtWidgets.QPushButton('Select Project')
        self.spider_combobox = QtWidgets.QComboBox()
        self.start_stop_button = QtWidgets.QPushButton("Start", checkable=True)
        self.text_edit = QtWidgets.QTextBrowser()
        self.input = QtWidgets.QLineEdit()
        self.input1 = QtWidgets.QLineEdit()
        self.input2 = QtWidgets.QLineEdit()
        self.input3 = QtWidgets.QLineEdit()
        self.input4 = QtWidgets.QLineEdit()
        self.input5 = QtWidgets.QLineEdit()
        self.input6 = QtWidgets.QLineEdit()
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)

        lay = QtWidgets.QVBoxLayout(central_widget)
        hlay = QtWidgets.QHBoxLayout()
        hlay.addWidget(self.project_le)
        hlay.addWidget(self.project_button)
        lay.addLayout(hlay)
        hlay2 = QtWidgets.QHBoxLayout()
        hlay2.addWidget(QtWidgets.QLabel("Input The Search Item :"))
        hlay2.addWidget(self.input, 1)
        hlay3 = QtWidgets.QHBoxLayout()
        hlay4 = QtWidgets.QHBoxLayout()
        hlay5 = QtWidgets.QHBoxLayout()
        hlay6 = QtWidgets.QHBoxLayout()
        hlay7 = QtWidgets.QHBoxLayout()
        hlay8 = QtWidgets.QHBoxLayout()
        hlay3.addWidget(QtWidgets.QLabel("Location :"))
        hlay3.addWidget(self.input1, 1 )
        hlay4.addWidget(QtWidgets.QLabel("Location 2 :"))
        hlay4.addWidget(self.input2, 1 )
        hlay5.addWidget(QtWidgets.QLabel("Location 3 :"))
        hlay5.addWidget(self.input3, 1 )
        hlay6.addWidget(QtWidgets.QLabel("Location 4 :"))
        hlay6.addWidget(self.input4, 1 )
        hlay7.addWidget(QtWidgets.QLabel("Location 5 :"))
        hlay7.addWidget(self.input5, 1 )
        hlay8.addWidget(QtWidgets.QLabel("Location 6 :"))
        hlay8.addWidget(self.input6, 1 )
        lay.addLayout(hlay2)
        lay.addLayout(hlay3)
        lay.addLayout(hlay4)
        lay.addLayout(hlay5)
        lay.addLayout(hlay6)
        lay.addLayout(hlay7)
        lay.addLayout(hlay8)
        lay.addWidget(self.start_stop_button)
        lay.addWidget(self.text_edit)

        self.start_stop_button.setEnabled(False)

        self.scrapy_worker = ScrapyWorker(self)
        self.scrapy_worker.logChanged.connect(self.insert_log)
        self.scrapy_worker.started.connect(self.text_edit.clear)
        self.scrapy_worker.finished.connect(partial(self.start_stop_button.setChecked, False))

        self.start_stop_button.toggled.connect(self.on_checked)
        self.project_button.clicked.connect(self.select_project)
        self.resize(640, 480)

    @QtCore.pyqtSlot(bool)
    def on_checked(self, state):
        if state:
            filename = self.project_le.text()
            finfo = QtCore.QFileInfo(filename)
            directory = finfo.dir().absolutePath()
            self.scrapy_worker.run(directory, self.spider_combobox.currentText())
            self.start_stop_button.setText('Stop')
        else:
            self.start_stop_button.setText('Start')
            self.scrapy_worker.stop()

    @QtCore.pyqtSlot()
    def select_project(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(
            self,
            "Select .cfg file",
            QtCore.QDir.currentPath(),
            "Configure File (*.cfg)"
        )
        if filename:
            self.project_le.setText(filename)
            finfo = QtCore.QFileInfo(filename)
            directory = finfo.dir().absolutePath()
            spiders = self.scrapy_worker.spiders(directory)
            self.spider_combobox.clear()
            self.spider_combobox.addItems(spiders)
            self.start_stop_button.setEnabled(True if spiders else False)

    @QtCore.pyqtSlot(str)
    def insert_log(self, text):
        prev_cursor = self.text_edit.textCursor()
        self.text_edit.moveCursor(QtGui.QTextCursor.End)
        self.text_edit.insertPlainText(text)
        self.text_edit.setTextCursor(prev_cursor)

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    app.setStyle('fusion')
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())