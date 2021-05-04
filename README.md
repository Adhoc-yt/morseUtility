# morseUtility
## Anything related to morse code

Ongoing project discussed and streamed on https://twitch.tv/adhoc_yt

So far, here's what it does:
- Translate clear text to Morse code
- Translate Morse code (with either 3 spaces or slashes) to clear text
- Generate Morse code sound (only plays it, not yet saving to file)

### Dependencies
```
pip install numpy
pip install pyaudio
```

### Example inputs
```
Message: - .... .. ... / .. ... / .- / - . ... -
Message: - .... .. ...   .. ...   .-   - . ... -
Message: This is a test
```

### TODOs
- Generate morse by clicking on a button (telegraph mode)
- Sound to morse to text
- Actual WPM (Words per minute) speed