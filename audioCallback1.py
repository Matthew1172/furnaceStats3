import pyaudio
import time
import numpy as np
import scipy.signal as signal
DURATION = 5
CHANNELS = 1
RATE = 44100

furnace_on = 0

p = pyaudio.PyAudio()
#b,a=signal.iirdesign(0.03,0.07,5,40)
fulldata = np.array([])

def callback(in_data, frame_count, time_info, flag):
    #global b,a,fulldata,furnace_on #global variables for filter coefficients and array
    global furnace_on, fulldata
    audio_data = np.fromstring(in_data, dtype=np.float32)
    #do whatever with data, in my case I want to hear my data filtered in realtime
    #audio_data = signal.filtfilt(b,a,audio_data,padlen=200).astype(np.float32).tostring()
    fulldata = np.append(fulldata,audio_data) #saves filtered data in an array
    #print(audio_data)
    #print(furnace_on)
    furnace_on+=1
    return (audio_data, pyaudio.paContinue)

stream = p.open(format=pyaudio.paFloat32,
                channels=CHANNELS,
                rate=RATE,
                output=True,
                input=True,
                stream_callback=callback)

stream.start_stream()

while stream.is_active():
    start = time.clock_gettime_ns()
    #time.sleep(DURATION)

    flag = False
    while not flag:
        inKey = input("Type any letter to stop recording")
        if inKey:
            flag = True


    stream.stop_stream()
stream.close()

p.terminate()


print(fulldata)