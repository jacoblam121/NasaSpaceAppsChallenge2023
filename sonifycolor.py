import wave
import struct
import math

def sonifycolor():
    color_dict = {
        'red': (255, 0, 0),
        'orange': (255, 165, 0),
        'yellow': (255, 255, 0),
        'green': (0, 128, 0),
        'blue': (0, 0, 255),
        'indigo': (75, 0, 130),
        'violet': (238, 130, 238),
        'black': (0, 0, 0)
    }

    # Define the frequency dictionary
    freq_dict = {
        (255, 0, 0): 293.66,
        (255, 165, 0): 329.63,
        (255, 255, 0): 349.23,
        (0, 128, 0): 392.00,
        (0, 0, 255): 440.00,
        (75, 0, 130): 493.88,
        (238, 130, 238): 554.37,
        (0, 0, 0): 261.63
    }

    def get_nearest_pure_color(rgb):
        distances = []
        for color in color_dict.values():
            distance = math.sqrt(sum([(a - b) ** 2 for a, b in zip(rgb, color)]))
            distances.append(distance)
        index = distances.index(min(distances))
        return list(color_dict.keys())[index]

    with open('rgb_values.txt') as f:
        rgb_values = [tuple(map(int, line.strip().split(','))) for line in f]

    pure_colors = [get_nearest_pure_color(rgb) for rgb in rgb_values]

    def get_frequency(color_name):
        rgb = color_dict[color_name]
        return freq_dict[rgb]

    def get_frequencies(color_names):
        return [get_frequency(color_name) for color_name in color_names]

    frequencies = get_frequencies(pure_colors)

    duration = 1

    sample_rate = 44100
    amplitude = 32767

    with wave.open('sonification_depth_of_coverage_colors.wav', 'w') as wave_file:

        wave_file.setparams((1, 2, sample_rate, sample_rate * duration * len(pure_colors), 'NONE', 'not compressed'))

        for frequency in frequencies:
            num_samples = int(sample_rate * duration)
            samples = [int(amplitude * math.sin(2 * math.pi * frequency * i / sample_rate)) for i in range(num_samples)]
            packed_samples = struct.pack('{}h'.format(num_samples), *samples)
            wave_file.writeframes(packed_samples)
