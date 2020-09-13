import time
import ctypes
import crcmod
from PyQt5.QtCore import pyqtSignal,QThread
import numpy as np
c_uint32 = ctypes.c_uint32
from protocolsTypes import *

class SendDataTreadClass(QThread):
    message = pyqtSignal(str)

    def __init__(self, main_class):
        super(SendDataTreadClass, self).__init__()
        self.main_class = main_class
        self.communicationState = main_class.communicationState
        self.old_frequency = self.main_class.frequencyLabel.text()
        self.bitfield = c_uint32(0)
        self.frequencySliderMaximum = self.main_class.frequencySlider.maximum()
        self.frequencySliderMinimum = self.main_class.frequencySlider.minimum()
        self.nPeriods = 32 # should be set by user
        self.packetsize = self.main_class.samplePerPeriod * self.nPeriods

    def run(self):
        while self.main_class.threadRunStatus:
            time.sleep(0.1)

            actual_frequency = self.main_class.frequencyLabel.text()

            if self.communicationState.getSendState():
                if self.main_class.checkBox_sweep.isChecked():

                    sliderValue = self.main_class.frequencySlider.value()
                    if sliderValue >= self.main_class.frequencySlider.maximum():
                        self.communicationState.setUpSweepDirection(False)
                    if sliderValue <= self.main_class.frequencySlider.minimum():
                        self.communicationState.setUpSweepDirection(True)

                    packet_size = self.packetsize
                    n_packet = self.calculateNpackets(sliderValue)
                    frequency_step = int(self.calculateFrequencyStep())
                    protocol = self.createProtocolDataAcquisition(packet_size, n_packet, frequency_step, int(self.main_class.frequencyToMCU))
                    self.communicationState.setSendState(False)
                else:
                    if self.old_frequency != actual_frequency:
                        print(actual_frequency)
                        self.setBit(self.bitfield, FREQUENCY_BIT)
                        print(bin(self.bitfield.value))
                        self.old_frequency = actual_frequency
                        protocol = self.createProtocolChange()
                        self.bitfield = c_uint32(0)
                    else:
                        packet_size = self.packetsize
                        n_packet = 1
                        frequency_step = 0
                        protocol = self.createProtocolDataAcquisition(packet_size,
                                                                      n_packet,
                                                                      frequency_step,
                                                                      int(self.main_class.frequencyToMCU))
                        # TODO default value for n_packet = 1, frequency_step = 0
                        self.communicationState.setSendState(False)

            if self.communicationState.getRepeatPrevMsgState():
                protocol = self.communicationState.getPrevSendMsg()
                self.communicationState.setRepeatPrevMsgState(False)

            if protocol:
                self.main_class.serialport.write(protocol)
                self.communicationState.prevSendMsg = protocol
                protocol = False
        self.main_class.sendDataComReadyToClose = True

    def createProtocolChange(self):
        head = bytearray([0xAA, UPDATE, 3, 0, 0, 0, 0, 0])

        bytefield = self.bitfield.value.to_bytes(4, 'little') #bytearray([0, self.bitfield.value])
        value_int = int(self.main_class.frequencyToMCU)
        value = value_int.to_bytes(4,'little')
        protocol = (head + bytefield + value + (0x55).to_bytes(1, 'little'))
        self.insert_lengt(protocol)
        return protocol

    def createProtocolDataAcquisition(self, packet_size, n_packet, frequency_step, actual_frequency):
        protocol_data_req = [0] * PROTOCOL_DATA_REQ_SIZE
        protocol_data_req[SIGNATURE_IDX] = SIGNATURE
        protocol_data_req[TYPE_IDX] = DATA_REQ
        protocol_data_req[SIZE_IDX] = HEAD_T_SIZE
        protocol_data_req[CRC_IDX] = 0
        protocol_data_req[PACKET_SIZE_IDX] = packet_size
        protocol_data_req[N_PACKET_IDX] = n_packet
        protocol_data_req[FREQUENCY_STEP_IDX] = frequency_step
        protocol_data_req[ACTUAL_FREQUENCY_IDX] = actual_frequency
        packet_protocol_data_req = protocol_data_req_t.pack(*protocol_data_req)

        protocol = bytearray((packet_protocol_data_req + (0x55).to_bytes(1, 'little')))

        self.insert_lengt(protocol)
        self.caltulate_and_insert_crc(protocol)

        return protocol

    def setBit(self, bitfield, bit):
        bitfield.value = bitfield.value | bit

    def insert_lengt(self, protocol):
        lenght = len(protocol)
        protocol[SIZE_IDX] = np.uint8(lenght)

    def caltulate_and_insert_crc(self, protocol):
        crc_Fun = crcmod.mkCrcFun(69665, initCrc=0x5ABE, rev=False)
        crc = crc_Fun(protocol)
        crc_byte = crc.to_bytes(4,'little')
        protocol[4] = np.uint8(crc_byte[0])
        protocol[5] = np.uint8(crc_byte[1])
        protocol[6] = np.uint8(crc_byte[2])
        protocol[7] = np.uint8(crc_byte[3])

    def calculateFrequencyStep(self):
        min_value = int(self.main_class.minFrequencyLineEdit.text())
        max_value = int(self.main_class.maxFrequencylineEdit.text())
        sliderMaxValue = self.main_class.frequencySlider.maximum()
        sliderSingleStep = self.main_class.frequencySlider.singleStep()

        frequency_range = max_value - min_value
        frequencyPerStep = frequency_range/sliderMaxValue
        frequencyStep = (frequencyPerStep / sliderSingleStep) * 5  # TODO remove 5 -> in visualizaton change size of buffers
        if self.communicationState.getUpSweepDirectionState():
            return frequencyStep
        else:
            return frequencyStep*(-1)

    def calculateNpackets(self, sliderValue):
        n_packets = 5 #TODO move setting this value in user interface if needed
        sweepUpDirection = self.communicationState.getUpSweepDirectionState()
        valueFromMinimum = sliderValue - self.frequencySliderMinimum
        valueFromMaximum = self.frequencySliderMaximum - sliderValue

        if sweepUpDirection:
            if n_packets*5 > valueFromMaximum:
                return int(valueFromMaximum/5)
            else:
                return n_packets
        else:
            if n_packets*5 > valueFromMinimum:
                return int(valueFromMinimum/5)
            else:
                return n_packets
