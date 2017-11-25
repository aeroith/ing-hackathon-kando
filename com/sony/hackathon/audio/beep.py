"""PyAudio Example: Play a wave file."""

import pyaudio
import wave
import sys
import threading
import time

CHUNK = 1024
MAX_DISTANCE = 2500


def beep(distance):
    if (distance < MAX_DISTANCE):
        sleep_amount = float(distance) * float(distance) / 1000000
        print sleep_amount
        time.sleep(sleep_amount)
        p = pyaudio.PyAudio()
        wf = wave.open('./beep.wav', 'rb')
        stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                        channels=wf.getnchannels(),
                        rate=wf.getframerate(),
                        output=True)
        data = wf.readframes(CHUNK)
        while len(data) > 0:
            stream.write(data)
            data = wf.readframes(CHUNK)
        stream.stop_stream()
        stream.close()
