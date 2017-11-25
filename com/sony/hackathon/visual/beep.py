"""PyAudio Example: Play a wave file."""

import pyaudio
import wave
import sys
import threading
import time

CHUNK = 1024
MAX_DISTANCE = 5000


def beep(distance):
    sleep_amount = float(distance) * float(distance) / 100000
    if sleep_amount < 5:
        time.sleep(sleep_amount/2)
        p = pyaudio.PyAudio()
        wf = wave.open('./beep-07.wav', 'rb')
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        data = wf.readframes(CHUNK)
        print "beep"
        while len(data) > 0:
            stream.write(data)
            data = wf.readframes(CHUNK)
        stream.stop_stream()
        stream.close()
        time.sleep(sleep_amount/2)

