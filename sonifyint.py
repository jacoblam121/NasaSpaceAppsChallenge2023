import numpy as np
from astropy.io import fits
import wave

def sonifyint():
    def sonify_fits(file_name):
        hdulist = fits.open(file_name)
        data = hdulist[0].data

        min_freq = 100  # Hz
        max_freq = 10000  # Hz

        log_scale = 10

        freqs = np.logspace(np.log10(min_freq), np.log10(max_freq), num=int(log_scale * data.max()), endpoint=True)

        amplitudes = data.flatten() / data.max()

        sample_rate = 44100  # Hz
        duration = 1.0  # seconds
        num_samples = int(sample_rate * duration)
        waveform = np.zeros(num_samples)
        for freq, amp in zip(freqs, amplitudes):
            t = np.linspace(0, duration, num_samples, endpoint=False)
            waveform += amp * np.sin(2 * np.pi * freq * t)

        waveform /= np.max(np.abs(waveform))

        samples = (waveform * 32767).astype(np.int16)

        return samples

    files = ['intensity_w1.fits', 'intensity_w2.fits', 'intensity_w3.fits', 'intensity_w4.fits']

    master_samples = np.array([], dtype=np.int16)
    for file in files:
        master_samples = np.append(master_samples, sonify_fits(file))

    with wave.open('sonification_intensity.wav', 'wb') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(44100)
        f.writeframes(master_samples.tobytes())