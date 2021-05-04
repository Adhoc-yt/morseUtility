# Morse code to text + text to morse code

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

DURATION_DOT = 1
DURATION_DASH = 3 * DURATION_DOT
DURATION_GAP = DURATION_DOT


def cleartext_to_morse(cleartext):
    if all(c in CLEARTEXT_TO_MORSE.keys() for c in cleartext):
        return ' '.join([CLEARTEXT_TO_MORSE[c] for c in cleartext])
    else:
        print('Invalid character - Cannot translate in morse code')
        return ''


def morse_to_cleartext(morse):
    return ''.join([MORSE_TO_CLEARTEXT[c] for c in morse.split(' ') if c != ''])


def morse_to_sound(morse):
    import time
    for c in morse:
        if c is '.':
            play_sound(DURATION_DOT)
        elif c is '-':
            play_sound(DURATION_DASH)
        else:
            # Play silence to separate characters
            play_silence()


def play_sound(duration):
    # https://github.com/faturita/python-toolbox/blob/master/PlaySound.py
    import pyaudio
    import numpy as np

    p = pyaudio.PyAudio()

    volume = 0.5  # range [0.0, 1.0]
    fs = 44100  # sampling rate, Hz, must be integer
    f = 550.0  # sine frequency, Hz, may be float

    samples = (np.sin(2 * np.pi * np.arange(fs * duration) * f / fs)).astype(np.float32)
    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=fs,
                    output=True)

    stream.write(volume * samples)
    stream.stop_stream()
    stream.close()

    p.terminate()


def play_silence():
    import time
    time.sleep(DURATION_GAP)


if __name__ == '__main__':
    message = input("Message: ")
    # if morse code then morse_to_cleartext
    if all(c in '.- ' for c in message):
        print(morse_to_cleartext(message))
    else:
        morsecode = cleartext_to_morse(message.upper())
        print(morsecode)
        morse_to_sound(morsecode)