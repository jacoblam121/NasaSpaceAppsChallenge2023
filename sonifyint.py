import numpy as np
from astropy.io import fits
import wave

def sonifyint():
    def sonify_fits(file_name):
        # Load the FITS file containing the intensity data
        hdulist = fits.open(file_name)
        data = hdulist[0].data

        # Define the frequency range for the sonification
        min_freq = 100  # Hz
        max_freq = 10000  # Hz

        # Define the logarithmic scaling factor
        log_scale = 10

        # Map the intensity values to frequencies using a logarithmic scale
        freqs = np.logspace(np.log10(min_freq), np.log10(max_freq), num=int(log_scale * data.max()), endpoint=True)

        # Map the intensity values to amplitudes
        amplitudes = data.flatten() / data.max()

        # Create a waveform from the frequency and amplitude arrays
        sample_rate = 44100  # Hz
        duration = 1.0  # seconds
        num_samples = int(sample_rate * duration)
        waveform = np.zeros(num_samples)
        for freq, amp in zip(freqs, amplitudes):
            t = np.linspace(0, duration, num_samples, endpoint=False)
            waveform += amp * np.sin(2 * np.pi * freq * t)

        # Scale the waveform to fit within [-1, 1]
        waveform /= np.max(np.abs(waveform))

        # Convert the waveform to samples
        samples = (waveform * 32767).astype(np.int16)

        return samples

    # List of files
    files = ['intensity_w1.fits', 'intensity_w2.fits', 'intensity_w3.fits', 'intensity_w4.fits']

    master_samples = np.array([], dtype=np.int16)
    for file in files:
        master_samples = np.append(master_samples, sonify_fits(file))

    # Write to WAV file
    with wave.open('../spaceapptestingrestore/spaceapptesting1/sonification_combined_back2back.wav', 'wb') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(44100)
        f.writeframes(master_samples.tobytes())