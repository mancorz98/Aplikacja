import nidaqmx
from nidaqmx import constants, stream_readers, stream_writers
import scipy.signal as signal

import time
import numpy as np
import matplotlib.pyplot as plt


def make_pulse(amp, dt, fs=10000, N=10000):
    """
    :param N:
    :param amp: amplituda pulsu
    :param dt: szerokosc pulsu
    :param fs: czestotliwosc probkowania
    :return: wektor wartości zadanych
    """
    ts = 1 / fs

    d_t = 1 / fs
    temp = N / fs
    t_i = np.linspace(-temp / 2, temp / 2, N)
    x = amp * (np.heaviside(t_i + dt / 2, 0.5) - np.heaviside(t_i - dt / 2, 0.5))
    """
    plt.plot(x)
    plt.show()
    """
    return x.reshape((1, N))


def zeroing(write_task, dt=1):
    """ Making a generation pause"""
    print('Zerowanie')
    write_task.write(0)
    time.sleep(dt)


def check_resistane(write_task: nidaqmx.Task, read_task: nidaqmx.Task,
                    writer: stream_writers.AnalogMultiChannelWriter, reader: stream_readers.AnalogMultiChannelReader,
                    r=4.7, amp=0.15, dt=0.01, fs=10000, N=1000):
    """ Generating a pulse for checking state of memristor """
    print('Sprawdzenie')
    writer.write_many_sample(make_pulse(amp, dt, fs=fs), timeout=100)
    buffer = np.zeros((2, N), dtype=np.float64)
    write_task.start()
    reader.read_many_sample(buffer, N, timeout=-1)

    write_task.wait_until_done()
    write_task.stop()
    U = buffer[0]
    I = buffer[1] / 4.7
    N = 2
    Wn = 0.1
    b, a = signal.butter(N, Wn, output='ba')

    U_f = signal.filtfilt(b, a, U[np.logical_not(np.logical_and(U < 0.02, U > -0.02))], method="gust")
    I_f = signal.filtfilt(b, a, I[(np.logical_not(np.logical_and(U < 0.02, U > -0.02)))], method="gust")
    """
    plt.figure(1)
    plt.title("Checking")
    f, (ax1, ax2) = plt.subplots(2,1)
    ax1.plot(I[(np.logical_not(np.logical_and(U < 0.02, U > -0.02)))])
    ax1.plot(I_f)
    ax2.plot(U)
    ax2.plot(I)
    plt.show()
    """

    R = U[np.logical_not(np.logical_and(U < 0.02, U > -0.02))] / I[
        (np.logical_not(np.logical_and(U < 0.02, U > -0.02)))]

    R_f = U_f / I_f
    R = R[R > 0]
    R_f = R_f[R_f > 0]
    print(f"R={np.mean(R)}, R_f={np.mean(R_f)}")

    return np.mean(R_f)


def set_Ron_state(write_task: nidaqmx.Task, read_task: nidaqmx.Task,
                  writer: stream_writers.AnalogMultiChannelWriter, reader: stream_readers.AnalogMultiChannelReader,
                  r=4.7, amp=0.15, dt=0.01, fs=10000, N=1000):
    """ Setting memristor in R_on state"""
    print('Ustawianie')
    writer.write_many_sample(make_pulse(amp, dt, fs=fs, N=N), timeout=-1)
    buffer = np.zeros((2, N), dtype=np.float64)
    write_task.start()
    reader.read_many_sample(buffer, N, timeout=100)

    write_task.wait_until_done()
    write_task.stop()
    U = buffer[0]
    I = buffer[1] / 4.7
    N = 2
    Wn = 0.1
    b, a = signal.butter(N, Wn, output='ba')

    U_f = signal.filtfilt(b, a, U[np.logical_not(np.logical_and(U < 0.02, U > -0.02))], method="gust")
    I_f = signal.filtfilt(b, a, I[(np.logical_not(np.logical_and(U < 0.02, U > -0.02)))], method="gust")

    I_s = signal.filtfilt(b, a, I, method="gust")
    peaks, _ = signal.find_peaks(I, height=np.mean(I), width=dt * N)
    #print(peaks)
    t_i = np.arange(start=0, step=1 / fs, stop=len(I_f) * 1 / fs, dtype=np.float64)
    q = np.trapz(x=t_i, y=I_f)
    # print(I_f)
    # print(U_f)
    p_i = np.multiply(U_f, I_f)
    E = np.trapz(x=t_i, y=p_i)
    print(f"q={q},\t E={E}")
    """
    plt.figure(1)
    plt.plot(I[(np.logical_not(np.logical_and(U < 0.02, U > -0.02)))])

    plt.plot(I_f)
    plt.title("Setting")
    plt.figure(2)
    plt.plot(U)
    plt.plot(I)
    plt.plot(peaks, I[peaks], "x")
    plt.title("Setting")
    plt.show()
    """
    return q, E


def set_Roff_state(write_task: nidaqmx.Task, writer: stream_writers.AnalogMultiChannelWriter, dt=0.1, amp=-1.5):
    """ Setting memristor in R_off state"""
    print('Resetowanie')
    writer.write_many_sample(make_pulse(amp, dt), timeout=100)
    write_task.start()
    write_task.wait_until_done()
    write_task.stop()


def check_state(r):
    """ Checking current state of memristor"""
    if r <= 3:
        return "R_on"
    elif r >= 50:
        return "R_off"
    else:
        return "Unknown"

def activation():

    with nidaqmx.Task() as task_write, nidaqmx.Task() as task_read:
        task_read.ai_channels.add_ai_voltage_chan("myDAQ1/ai0", "channel1", constants.TerminalConfiguration.DIFF, -5, 5)
        task_read.ai_channels.add_ai_voltage_chan("myDAQ1/ai1", "channel2", constants.TerminalConfiguration.DIFF, -5, 5)
        task_write.ao_channels.add_ao_voltage_chan("myDAQ1/ao0", 'write_channel', -2.5, 2.5)
        task_read.timing.cfg_samp_clk_timing(rate=fs_acq, samps_per_chan=N,
                                            sample_mode=constants.AcquisitionType.FINITE)  # you may not need samps_per_chan
        task_write.timing.cfg_samp_clk_timing(rate=fs_acq, samps_per_chan=N, sample_mode=constants.AcquisitionType.FINITE,
                                            active_edge=constants.Edge.FALLING)
        samples_per_buffer = int(fs_acq // 1)
        task_read.in_stream.input_buf_size = samples_per_buffer * 10  # plus some extra space
        task_write.out_stream.output_buf_size = samples_per_buffer * 10
        reader = stream_readers.AnalogMultiChannelReader(task_read.in_stream)
        writer = stream_writers.AnalogMultiChannelWriter(task_write.out_stream, auto_start=False)
