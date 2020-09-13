import sys
import gui
import serial
import glob
from receiveDataThreadFile import ReceiverDataTreadClass
from sendDataThreadFile import SendDataTreadClass
from Comunication_states import CommunicationStates_class
from time import sleep

from PyQt5.QtWidgets import*
from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)


class MainClass(QMainWindow, gui.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.frequencySlider.valueChanged.connect(self.frequencySlider_change)

        #communication state
        self.communicationState = CommunicationStates_class()
        ports = self.serial_ports()
        print(ports)
        for x in ports:
            self.comportComboBox.addItem(x)

        self.startStopButton.clicked.connect(self.startAnalyse)

        self.frequencyToMCU = 50000
        self.samplePerPeriod = 16 #should be send in init msg when init msg will be created and set by user

        self.addToolBar(NavigationToolbar(self.MplWidget_phase.canvas, self))

        self.checkBox_sweep.stateChanged.connect(self.sweep)

        self.threadRunStatus = False
        self.sendDataComReadyToClose = False
        self.receiveDataComReadyToClose = False

    def frequencySlider_change(self):
        value = self.frequencySlider.value()
        min_value = int(self.minFrequencyLineEdit.text())
        max_value = int(self.maxFrequencylineEdit.text())
        self.frequencyToMCU = min_value + (max_value-min_value)*value*0.001
        self.frequencyLabel.setText(str(self.frequencyToMCU))

    def sweep(self):
        if self.checkBox_sweep.isChecked() == True:
            self.minFrequencyLineEdit.setReadOnly(True)
            self.maxFrequencylineEdit.setReadOnly(True)
            self.frequencySlider.setValue(self.frequencySlider.minimum())
            print("set")
        else:
            self.minFrequencyLineEdit.setReadOnly(False)
            self.maxFrequencylineEdit.setReadOnly(False)
            print("reset")

    def serial_ports(self):
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result

    def startAnalyse(self):

        #TODO if needed send stop_hrtim mesg (need create mesg)

        if self.startStopButton.text() == 'START':
            self.frequencySlider.setEnabled(True)
            self.maxFrequencylineEdit.setEnabled(False)
            self.minFrequencyLineEdit.setEnabled(False)
            self.checkBox_sweep.setEnabled(True)
            self.threadRunStatus = True
            self.receiveDataComReadyToClose = False
            self.sendDataComReadyToClose = False
            self.startStopButton.setText('STOP')

            self.serialport = serial.Serial()
            self.serialport.baudrate = 115200
            self.serialport.port = str(self.comportComboBox.currentText())
            self.serialport.timeout = 3
            #        self.serialport.parity = serial.PARITY_NONE
            #        self.serialport.stopbits = serial.STOPBITS_ONE
            #        self.serialport.bytesize = serial.SEVENBITS
            self.serialport.open()

            self.mySerial = ReceiverDataTreadClass(self)
            self.mySerial.setPriority(self.mySerial.HighestPriority)
            self.mySerial.start()

            self.update = SendDataTreadClass(self)
            self.update.start()

        elif self.startStopButton.text() == 'STOP':

            self.threadRunStatus = False
            self.checkBox_sweep.setChecked(False)
            while (self.receiveDataComReadyToClose != True) and (self.sendDataComReadyToClose != True):
                pass
            sleep(0.5)
            self.serialport.close()

            self.frequencySlider.setEnabled(False)
            self.maxFrequencylineEdit.setEnabled(True)
            self.minFrequencyLineEdit.setEnabled(True)
            self.checkBox_sweep.setEnabled(False)
            self.startStopButton.setText('START')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainClass()
    win.show()
    app.exec_()
