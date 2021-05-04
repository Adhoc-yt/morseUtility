# Dictionary morse code -> clear text
CLEARTEXT_TO_MORSE = {'A': '.-',
                      'B': '-...',
                      'C': '-.-.',
                      'D': '-..',
                      'E': '.',
                      'F': '..-.',
                      'G': '--.',
                      'H': '....',
                      'I': '..',
                      'J': '.---',
                      'K': '-.-',
                      'L': '.-..',
                      'M': '--',
                      'N': '-.',
                      'O': '---',
                      'P': '.--.',
                      'Q': '--.-',
                      'R': '.-.',
                      'S': '...',
                      'T': '-',
                      'U': '..-',
                      'V': '...-',
                      'W': '.--',
                      'X': '-..-',
                      'Y': '-.--',
                      'Z': '--..',
                      '1': '.----',
                      '2': '..---',
                      '3': '...--',
                      '4': '....-',
                      '5': '.....',
                      '6': '-....',
                      '7': '--...',
                      '8': '---..',
                      '9': '----.',
                      '0': '-----',
                      ',': '--..--',
                      '.': '.-.-.-',
                      '?': '..--..',
                      '/': '-..-.',
                      '-': '-....-',
                      '(': '-.--.',
                      ')': '-.--.-',
                      ' ': ' '}
# Reverse dictionary
MORSE_TO_CLEARTEXT = {value: key for key, value in CLEARTEXT_TO_MORSE.items()}

# Speed of sound output
WPM = 4


def cleartext_to_morse(cleartext):
    if all(c in CLEARTEXT_TO_MORSE.keys() for c in cleartext):
        return ' '.join([CLEARTEXT_TO_MORSE[c] for c in cleartext])
    else:
        print('Invalid character - Cannot translate in morse code')
        return ''


def morse_to_cleartext(morse):
    cleartext = ''
    for word in morse.split('   '):
        for c in word.split(' '):
            if c in MORSE_TO_CLEARTEXT.keys():
                cleartext += MORSE_TO_CLEARTEXT[c]
        cleartext += ' '
    return cleartext.lower().capitalize()


def morse_to_sound(morse):
    import pyaudio
    import numpy as np

    p = pyaudio.PyAudio()
    volume = 0.5  # [0.0, 1.0]
    fs = 44100  # sampling rate, Hz, int
    f = 600.0  # sine frequency, Hz, float
    duration_dot = 1 * WPM/10
    duration_dash = 3 * duration_dot
    duration_gap = 1 * duration_dot

    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=fs,
                    output=True)
    sample_dot = (np.sin(2 * np.pi * np.arange(fs * duration_dot) * f / fs)).astype(np.float32)
    sample_dash = (np.sin(2 * np.pi * np.arange(fs * duration_dash) * f / fs)).astype(np.float32)
    sample_gap = (np.sin(2 * np.pi * np.arange(fs * duration_gap) * 0 / fs)).astype(np.float32)
    sample_space = (np.sin(2 * np.pi * np.arange(fs * duration_dash) * 0 / fs)).astype(np.float32)

    samples = []
    for c in morse:
        if c is '.':
            samples.append(sample_dot)
            samples.append(sample_gap)
        elif c is '-':
            samples.append(sample_dash)
            samples.append(sample_gap)
        else:
            samples.append(sample_space)

    for sample in samples:
        stream.write(volume * sample)

    stream.stop_stream()
    stream.close()
    p.terminate()


def play_silence():
    import time
    time.sleep(duration_gap)


if __name__ == '__main__':
    message = input("Message: ")
    # if morse code then morse_to_cleartext
    if all(c in '.- /' for c in message):
        print(morse_to_cleartext(message.replace('/', ' ')))
    else:
        morsecode = cleartext_to_morse(message.upper())
        print(morsecode)
        morse_to_sound(morsecode)
