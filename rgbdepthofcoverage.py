import numpy as np
from astropy.io import fits
import matplotlib.pyplot as plt
import itertools
from PIL import Image

def rgbdepthofcoverage():
    def load_fits_data(filename):
        """Load the image data from a FITS file."""
        with fits.open(filename) as hdul:
            data = hdul[0].data.astype(float)
            data = (data - np.min(data)) / (np.max(data) - np.min(data))
        return data

    red_channel = load_fits_data('depth_of_coverage_1.fits')
    green_channel = load_fits_data('depth_of_coverage_2.fits')
    blue_channel = load_fits_data('depth_of_coverage_3.fits')

    combinations = list(itertools.permutations([red_channel, green_channel, blue_channel]))
    for i, combination in enumerate(combinations):
        cov_image = np.stack(combination, axis=-1)
        # Display the RGB image using matplotlib
        plt.imshow(cov_image, origin='lower')
        plt.axis('off')
        plt.savefig(f'rgb_{i}.png', bbox_inches='tight', pad_inches=0)

def rgbpngtotxt():

    rgb_values = []
    for i in range(6):
        cov_image = Image.open(f'rgb_{i}.png')
        rgb_values.append(cov_image.getpixel((20, 20)))

    with open('rgb_values.txt', 'w') as f:
        for rgb in rgb_values:
            f.write(f'{rgb[0]}, {rgb[1]}, {rgb[2]}\n')


