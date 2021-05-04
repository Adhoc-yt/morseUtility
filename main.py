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
WPM = 20
SOUND_VOLUME = 0.5  # [0.0, 1.0]
CHUNK = 1024


def yes_no(question):
    while "Invalid answer":
        reply = str(input(question+' (y/n): ')).lower().strip()
        if reply[:1] == 'y':
            return True
        if reply[:1] == 'n':
            return False


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
    fs = 44100  # sampling rate, Hz, int
    f = 600.0  # sine frequency, Hz, float
    duration_dot = 12 / (10 * WPM)  # 20 words per minute = 60 ms
    duration_dash = 3 * duration_dot
    duration_gap = 1 * duration_dot

    stream = p.open(format=pyaudio.paFloat32,
                    channels=1,
                    rate=fs,
                    output=True,
                    frames_per_buffer=CHUNK)
    sample_dot = (np.sin(2 * np.pi * np.arange(fs * duration_dot) * f / fs)).astype(np.float32)
    sample_dash = (np.sin(2 * np.pi * np.arange(fs * duration_dash) * f / fs)).astype(np.float32)
    sample_gap = (np.sin(2 * np.pi * np.arange(fs * duration_gap) * 0 / fs)).astype(np.float32)
    sample_space = (np.sin(2 * np.pi * np.arange(fs * duration_dash) * 0 / fs)).astype(np.float32)

    frames = []
    for c in morse:
        if c is '.':
            frames.append(sample_dot)
            frames.append(sample_gap)
        elif c is '-':
            frames.append(sample_dash)
            frames.append(sample_gap)
        else:
            frames.append(sample_space)

    stream.stop_stream()
    stream.close()
    p.terminate()

    if yes_no("Save sound?"):
        filename = input("Filename (*.wav): ")
        if not filename.endswith(".wav"):
            filename = filename + ".wav"
        save_wav_file(filename, p.get_sample_size(pyaudio.paFloat32), fs, frames)
        if yes_no("Play '" + filename + "'?"):
            play_wav_file(filename)
    elif yes_no("Play sound?"):
        filename = input("Filename: ")
        play_wav_file(filename)


def save_wav_file(filename, sample_width, rate, frames):
    import wave
    wf = wave.open(filename, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(sample_width)
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()


def play_wav_file(filename):
    import wave
    import pyaudio
    wf = wave.open(filename, 'rb')
    p = pyaudio.PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    frames = wf.readframes(CHUNK)
    while frames != b'':
        stream.write(frames)
        frames = wf.readframes(CHUNK)

    stream.close()
    p.terminate()


if __name__ == '__main__':
    message = input("Message: ")
    # if morse code then morse_to_cleartext
    if all(c in '.- /' for c in message):
        print(morse_to_cleartext(message.replace('/', ' ')))
    else:
        morsecode = cleartext_to_morse(message.upper())
        print(morsecode)
        morse_to_sound(morsecode)
