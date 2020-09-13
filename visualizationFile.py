from protocolsTypes import *
import numpy as np
import scipy.fftpack

class VisualizationClass:
    def __init__(self, main_class):
        self.main_class = main_class
        self.MplWidget_phase = main_class.MplWidget_phase

        self.MplWidget_phase.canvas.axes = self.MplWidget_phase.canvas.figure.add_subplot(311)
        self.MplWidget_phase.canvas.axes2 = self.MplWidget_phase.canvas.figure.add_subplot(312)
        self.MplWidget_phase.canvas.axes3 = self.MplWidget_phase.canvas.figure.add_subplot(313)

        self.min_value = int(self.main_class.minFrequencyLineEdit.text())
        self.max_value = int(self.main_class.maxFrequencylineEdit.text())

        self.angleArray = np.empty(201)
        self.angleArray[:] = np.NaN
        self.angleArray[0] = 0
        self.angleArray[200] = 0

        self.magArray = np.empty(201)
        self.magArray[:] = np.NaN
        self.magArray[0] = 0
        self.magArray[200] = 0

    def update_graph(self, data):

        protocol_data_resp = protocol_data_resp_t.unpack(data[:protocol_data_resp_t.size])
        actual_frequency = protocol_data_resp[ACTUAL_FREQUENCY_IDX]

        frequencyPerStep = (self.max_value-self.min_value)/self.main_class.frequencySlider.maximum()
        position_step = int(protocol_data_resp[FREQUENCY_STEP_IDX] / frequencyPerStep)
        position_in_array = int((actual_frequency - int(self.main_class.minFrequencyLineEdit.text()))/frequencyPerStep) - position_step*protocol_data_resp[N_PACKET_IDX]

        length_of_signal = protocol_data_resp[PACKET_SIZE_IDX]
        sample = length_of_signal * BYTE_PER_SAMPLE
        min_value = int(self.main_class.minFrequencyLineEdit.text())
        max_value = int(self.main_class.maxFrequencylineEdit.text())
        phase_x = np.linspace(min_value, max_value, 201)

        for z in range(0, protocol_data_resp[N_PACKET_IDX], 1):

            samples = []
            for x in range(0, sample, 2):
                adc_sample = int.from_bytes(data[protocol_data_resp_t.size+x + (z*length_of_signal): protocol_data_resp_t.size+BYTE_PER_SAMPLE+x + (z*length_of_signal)], byteorder='little')
                adc_sample = (adc_sample*3.3)/4095
                samples.append(adc_sample)

            N = length_of_signal
            actual_frequency = float(self.main_class.frequencyLabel.text())
            T = actual_frequency * self.main_class.samplePerPeriod/2
            yf = scipy.fftpack.fft(samples)
            xf = np.linspace(0.0, int(N/2),  int(N/2))*T/N
            yf = yf[:N // 2]
            fft_value = 2.0 / N * np.abs(yf)

            phase = np.angle(yf[int(sample / self.main_class.samplePerPeriod)])
            if phase < 0:
                #np.pi/self.main_class.samplePerPeriod because miss one trigger point in synchronication
                phase = phase + np.pi - np.pi/self.main_class.samplePerPeriod
            elif phase > 0:
                #np.pi/self.main_class.samplePerPeriod because miss one trigger point in synchronication
                phase = phase - np.pi - np.pi/self.main_class.samplePerPeriod
            magnitude = fft_value[0] / 2 + fft_value[int(sample / self.main_class.samplePerPeriod)]
            self.angleArray[int((position_in_array + position_step*z)/5)] = phase
            self.magArray[int((position_in_array + position_step*z)/5)] = magnitude
            fft_value[0] = 0

        self.MplWidget_phase.canvas.axes.clear()
        self.MplWidget_phase.canvas.axes2.clear()
        self.MplWidget_phase.canvas.axes3.clear()

        self.MplWidget_phase.canvas.axes.set_title('fft of square wave ' + str(actual_frequency) + 'Hz')
        self.MplWidget_phase.canvas.axes.set_xlabel('frequency')
        self.MplWidget_phase.canvas.axes.set_ylabel('power signal')

        self.MplWidget_phase.canvas.axes2.set_xlabel('frequency')
        self.MplWidget_phase.canvas.axes2.set_ylabel('Magnitute')

        self.MplWidget_phase.canvas.axes3.set_xlabel('frequency')
        self.MplWidget_phase.canvas.axes3.set_ylabel('Phase')

        self.MplWidget_phase.canvas.axes.plot(xf, fft_value)
        self.MplWidget_phase.canvas.axes2.plot(phase_x, self.magArray, 'ro', markersize=1)
        self.MplWidget_phase.canvas.axes3.plot(phase_x, self.angleArray, 'ro', markersize=1)

        self.MplWidget_phase.canvas.draw()
