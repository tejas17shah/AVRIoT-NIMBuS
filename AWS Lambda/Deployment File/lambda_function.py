import json
import boto3
import numpy as np
from scipy import signal
from scipy.fft import fft,fftfreq 

def lambda_handler(event, context):
    # TODO implement
    data = event['B']
    data = [i * 5 for i in data]
    data = [i / 1024 for i in data]
    
    N = 64
    SAMPLE_RATE = 10
    CF = 6000
    
    data = np.pad(data, (0,4), 'constant', constant_values=(0)) 
    
    # Digital Filtering
    sos = signal.butter(15,0.2,'hp', fs=SAMPLE_RATE, output='sos')
    filtered = signal.sosfilt(sos, data)

    # fft 
    transformed = fft(filtered)
    yf = np.abs(transformed[:N//2])
    xf = fftfreq(128, 1 / SAMPLE_RATE)
    yf = yf/N
    xf = xf[:64]
    
    peaks, _ = signal.find_peaks(yf, height=0)
    
    bgPeak = np.max(yf[peaks]) 
    
    heartRateTemp = np.where(yf == bgPeak)
    heartRate = xf[heartRateTemp] * 60
    print(bgPeak*CF,heartRate)

    return 0
