from PyQt5.QtCore import pyqtSignal,QThread
import numpy as np
from visualizationFile import VisualizationClass
from protocolsTypes import *
import crcmod


class ReceiverDataTreadClass(QThread):
    message = pyqtSignal(str)

    def __init__(self, main_class):
        super(ReceiverDataTreadClass, self).__init__()
        self.serialport = main_class.serialport
        self.main_class = main_class
        self.communicationState = main_class.communicationState

        self.buf = bytearray()
        self.protocol = False

    def run(self):
        self.visualization = VisualizationClass(self.main_class)
        while self.main_class.threadRunStatus:
            protocol = self.readprotocol
            if self.calculateAndCheckCRC(protocol):
                self.visualization.update_graph(protocol)
            else:
                self.communicationState.setRepeatPrevMsgState(True)

            print(self.main_class.frequencyLabel.text())
            if self.main_class.checkBox_sweep.isChecked():
                self.change_frequency_for_sweep(protocol)
            self.communicationState.setSendState(True)
        self.main_class.receiveDataComReadyToClose = True
        del self.visualization

    @property
    def readprotocol(self):
        while True:
            i = 1 # olways read only first byte in queue
            data = self.serialport.read(i)
            if data:
                if data[0].to_bytes(1, 'little') == (0xaa).to_bytes(1, 'little'):
                    self.protocol = True
                    self.buf[0:] = data[1+1:]

            if self.protocol:
                self.buf.extend(data)
                data = self.serialport.read_until((0x55555555).to_bytes(4, 'little'))
                self.buf.extend(data)
                self.protocol = False
                r = self.buf
                return r
            else:
                i = data.find(b"\n")

            if i >= 0:
                self.protocol = False
                r = self.buf + data[:i+1]
                self.buf[0:] = data[i+1:]
                return r
            else:
                self.buf.extend(data)

    def change_frequency_for_sweep(self, protocol):
        protocol_head = protocol_data_resp_t.unpack(protocol[:protocol_data_resp_t.size])

        actual_frequency = protocol_head[ACTUAL_FREQUENCY_IDX]
        min_value = int(self.main_class.minFrequencyLineEdit.text())
        max_value = int(self.main_class.maxFrequencylineEdit.text())

        frequencyPerStep = (max_value-min_value)/self.main_class.frequencySlider.maximum()
        sliderValue = (actual_frequency - min_value)/frequencyPerStep

        self.main_class.frequencySlider.setValue(sliderValue)
        self.main_class.frequencySlider_change()

    def calculateAndCheckCRC(self, protocol):
        protocol_head = head_t.unpack(protocol[:head_t.size])
        crc_source = protocol_head[CRC_IDX]
        protocol[4] = np.uint8(0)
        protocol[5] = np.uint8(0)
        protocol[6] = np.uint8(0)
        protocol[7] = np.uint8(0)
        crc_Fun = crcmod.mkCrcFun(69665, initCrc=0x5ABE, rev=False)
        crc = crc_Fun(protocol)
        status = crc_source == crc
        return status
