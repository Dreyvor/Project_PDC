import txt_binary as tb
import BinaryToCodeword as b2c
import CodewordToBinary as c2b
import numpy as np

##################################################################
def textToCodewords(txt):
    bits = tb.text_to_bits(txt)
    codeword = b2c.f(bits)
    return codeword

def codewordToText(codeword):
    bits2 = c2b.f(codeword)
    res = tb.text_from_bits(bits2)
    return res

##################################################################
#Define Psi(t)

beta = 1/2.0
#T_psi : good values begin at 1/400
T_psi = 1/600.0 # we want it small
print("The frequency-band will have a width of approximately:",1/T_psi,"Hz")

def psi(t):
    c = 1.0 - np.square(4.0 * beta * t / T_psi)
    
    temp_error = np.geterr()
    np.seterr(divide='ignore', invalid='ignore')
    res = np.where(np.abs(c) <= 1E-2,
                   (beta / (np.pi * np.sqrt(2 * T_psi)))
                   * ((np.pi + 2) * np.sin(np.pi / (4 * beta))
                      +(np.pi - 2) * np.cos(np.pi / (4 * beta))),
                   
                   (4.0 * beta)/(np.pi * np.sqrt(T_psi))
                   * (np.cos((1.0 + beta) * np.pi * t / T_psi)
                      + ((1.0 - beta) * np.pi) / (4.0 * beta) * np.sinc((1.0 - beta) * t / T_psi))
                   / c
                   )
    np.seterr(divide='warn', invalid='warn')  
    return res

# Init some variables
ff = 2000 # frequency of the signal in Hz
Fs = 22050 # given
Ts = 1.0/Fs # sampling interval
time_interval = 0.003
t = np.arange(-time_interval, time_interval, Ts) # time vector

# Modulate Psi(t) to get a signal base
# Modulate a given signal to 2000Hz, 4000Hz, 6000Hz and 8000Hz and resize it to [-1,1]
def modulate_and_resize(signal):
    y = signal * np.cos(2*np.pi*ff*t) + signal * np.cos(2*2*np.pi*ff*t) + signal * np.cos(3*2*np.pi*ff*t) + signal * np.cos(4*2*np.pi*ff*t)
    ymax = np.max(np.abs(y))
    y /= ymax
    return y

def getSignal():
    y = modulate_and_resize(psi(t))
    return y

# base represents the base wave modulated at 4 different frequencies
base = modulate_and_resize(psi(t))
base_len = len(base)


####################################################################
# ENCODING

def encode(list_codewords, base):
    base_length = len(base)
    signal = np.zeros(len(list_codewords) * base_length)
    
    for i in range(len(list_codewords)):
        for j in range(base_length):
            signal[i * base_length + j] = list_codewords[i] * base[j]
    
    # Add start clap
    signal_with_clap_start = []
    for i in range(len(signal) + len(clap_start)):
        if(i < len(clap_start)):
            signal_with_clap_start.append(clap_start[i])
        else:
            signal_with_clap_start.append(signal[i-len(clap_start)])
            
    # Add clap end
    signal_with_clap_start_end = []
    for i in range(len(signal_with_clap_start) + len(clap_end)):
        if(i < len(signal_with_clap_start)):
            signal_with_clap_start_end.append(signal_with_clap_start[i])
        else:
            signal_with_clap_start_end.append(clap_end[i-len(signal_with_clap_start)])
    
    return signal_with_clap_start_end

#Reload claps
clap_start = np.loadtxt("clap_start.txt")
clap_end = np.loadtxt("clap_end.txt")
clap_len = len(clap_start)

#####################################################################
# PARAMETER ESTIMATION

def findOffset(signal_received, signal_desired, b):
    signal_desired_length = len(signal_desired)
    a = []
    for i in range(len(signal_received) - signal_desired_length):
        temp = 0
        for j in range(signal_desired_length):
            temp += signal_received[i+j] * signal_desired[j]
        a.append(temp)
    toReturn = 0
    if(b):
        toReturn = min(len(signal_received) - base_len, np.argmax(np.abs(a)))
    else:
        toReturn = np.argmax(np.abs(a))
    return toReturn

def offsets(rcv_signal):
    clap_start = np.loadtxt("clap_start.txt")
    clap_end = np.loadtxt("clap_end.txt")
    start = findOffset(rcv_signal, clap_start, False)
    end = findOffset(rcv_signal, clap_end, True)
    #verify multiple of 8 * 133 (8 bits * len(base)), else take more/less values at the end
    mod = (end-start) % (8*base_len)
    if(mod != clap_len): #must be clap_len and not 0, because we count clap_start (length 133)
        temp = 0
        if(mod >= 133 + ((8*base_len) // 2)):
            temp = end + (8*base_len - mod)
        else:
            temp = end - mod
        end = temp
    res = [start,end]
    return res

#####################################################################
# DECODING

import time
import os

def decode(rcv_signal, base):
    base_len = len(base)
    
    now = time.time()
    
    tab_offsets = offsets(rcv_signal)
    
    after = time.time()
    print("### Time to compute parameters :", after - now)
    
    offset_start = tab_offsets[0] + clap_len
    offset_end = tab_offsets[1]
    
    decoded = []
    for i in range(offset_start, offset_end + 1, base_len):
        temp = 0
        for j in range(base_len):
            temp += rcv_signal[i + j] * base[j]
        decoded.append(temp)
    return decoded

def receiver(decoded):
    #Decision rule
    for i in range(len(decoded)):
        if (decoded[i] > 0):
            decoded[i] = 1
        else:
            decoded[i] = -1
            
    temp = len(decoded) // 8
    final_res = codewordToText(decoded[:temp*8])
    return final_res

def main(s):
    code = b2c.f(tb.text_to_bits(s))
    signal = encode(code, base)
    
    np.savetxt("to_send.txt", signal)
    cmd_send_to_srv = 'python client.py --input_file=to_send.txt --output_file=received.txt --srv_hostname=iscsrv72.epfl.ch --srv_port=80'
    
    os.system(cmd_send_to_srv)
    
    print("### String sent.")

    received = np.loadtxt("received.txt")
    decoded = decode(received, base)
    final_res = receiver(decoded)

    return final_res


#################################################################
# Start the machine

given_str = "I don't know half of you half as well as I should like; and I like less than half of you half as well as you deserve."
print("Sending:\n", given_str)
print("Decoded:\n",main(given_str))
