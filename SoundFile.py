import pyaudio
import wave
import numpy as np
from matplotlib import pyplot as plt
from scipy import signal
from scipy.io import wavfile

SOUND_VOLUME = 0.5  # [0.0, 1.0]
WPM = 20


class SoundFile:
    chunk = 1024
    fs = 44100  # sampling rate, Hz, int
    f = 600.0  # sine frequency, Hz, float
    duration_dot = 12 / (10 * WPM)  # 20 words per minute = 60 ms
    duration_dash = 3 * duration_dot
    duration_gap = 1 * duration_dot

    def __init__(self, filename):
        self.filename = filename
        self.wf = wave.open(filename, 'rb')
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.p.get_format_from_width(self.wf.getsampwidth()),
                                  channels=self.wf.getnchannels(),
                                  rate=self.wf.getframerate(),
                                  output=True)

    @staticmethod
    def save_wav_file(filename, sample_width, rate, frames):
        import wave
        wf = wave.open(filename, 'wb')
        wf.setnchannels(1)
        wf.setsampwidth(sample_width)
        wf.setframerate(rate)
        wf.writeframes(b''.join(frames))
        wf.close()

    def play(self):
        frames = self.wf.readframes(self.chunk)
        while frames != b'':
            self.stream.write(frames)
            frames = self.wf.readframes(self.chunk)

    def close(self):
        self.stream.close()
        self.p.terminate()

    def get_frequency_spectrum(self):
        sample_rate, samples = wavfile.read(self.filename)
        frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate)

        plt.subplots_adjust(bottom=0, left=0, top=1, right=1)
        plt.pcolormesh(times, frequencies, spectrogram)
        plt.imshow(spectrogram)
        plt.ylabel('Frequency [Hz]')
        plt.xlabel('Time [sec]')
        plt.show()
