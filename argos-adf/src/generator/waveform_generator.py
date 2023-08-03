import matplotlib.pyplot as plt
import numpy as np
from scipy import signal

from model import ArgosData
from helper.utils import data_parser


class WaveformGenerator:
    def __init__(self, amplitude, frequency, second, resolution):
        self._amp = amplitude
        self._freq = frequency
        self._sec = second
        self._rez = resolution

        self._t = np.linspace(0, self._sec, self._sec / self._rez)
        self._w = np.sin(self._amp * np.pi * self._freq * (self._t / self._rez)) + self._amp

    def fetch(self):
        argos_data = ArgosData()
        argos_data.data = list(map(list, zip(self._w, self._t)))
        argos_data.resolution = self._rez
        argos_data.start = 0
        argos_data.end = self._sec

        return argos_data

    def _f(self, x):
        y = 0
        result = []
        for _ in x:
            result.append(y)
            y = y + np.random.normal(scale=1)
        return np.array(result)

    def _smooth(self, x, N):
        return np.convolve(x, np.ones((N,)) / N)[(N - 1):]


class WaveformGenerator(DataGenerator):
    def __init__(self, amplitude1, frequency1, second, resolution,
                 amplitude2, frequency2, start, end, waveform=None):
        if waveform is None:
            raise ValueError
        self._w[start: end + 1] = (
            waveform(amplitude2 * np.pi * frequency2 * (self._t / self._rez)) + amplitude2
        )[start: end + 1]
        super().__init__(amplitude1, frequency1, second, resolution)


if __name__ == "__main__":
    sawtooth_generator = WaveformGenerator(
        amplitude1=1,
        frequency1=10,
        second=3600,
        resolution=1,
        amplitude2=2,
        frequency2=5,
        start=2160,
        end=2160 + 360,
        waveform=signal.sawtooth,
    )
    argos_data = sawtooth_generator.fetch()

    w, t = data_parser(argos_data.data)

    plt.figure(figsize=(10.5, 4.5))
    plt.plot(t, w)
    plt.margins(0.1, 0.1)
    plt.grid(True)
    plt.show()
