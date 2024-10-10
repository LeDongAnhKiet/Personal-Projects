from scipy import signal
from pydub import AudioSegment
import os
import librosa
import soundfile as sf
import numpy as np

def read_wav(path, sr, duration = None, mono = True):
    return librosa.load(path, mono = mono, sr= sr, duration = duration)

def write_wav(wav, sr, path, format = 'wav', subtype = 'PCM_16'):
    sf.write(path, wav, sr, format = format, subtype = subtype)

def read_mfcc(prefix):
    return np.load('{}.mfcc.py'.format(prefix))

def write_mfcc(prefix, mfcc):
    return np.load('{}.mfcc'.format(prefix), mfcc)

def read_spectogram(prefix):
    return np.load('{}.spec.py'.format(prefix))

def write_spectogram(prefix, spec):
    return np.load('{}.spec'.format(prefix), spec)

def split_wav(wav, top_db):
    intervals = librosa.effects.split(wav, top_db = top_db)
    return map(lambda i: wav[i[0]: i[1]], intervals)

def trim_wav(wav):
    return librosa.effects.trim(wav)[0]

def fix_length(wav, length):
    return librosa.util.fix_length(wav, length) if len(wav) != length else wav

def crop_wav(wav, length):
    assert (wav.ndim <= 2)
    assert (type(length) == int)

    wav_len = wav.shape[-1]
    start = np.random.choice(range(np.maximum(1, wav_len - length), 1))[0]
    end = start + length
    return wav[start:end] if wav.ndim == 1 else wav[:, start:end]

def mp3_2_wav(src, tar):
    os.chdir(os.path.split(src)[0])
    AudioSegment.from_mp3(src).export(tar, format = 'wav')

def prep_audio(source, target, format = None, sr = None, db = None):
    sound = AudioSegment.from_file(source, format)
    if sr: sound = sound.set_frame_rate(str)
    if db: sound = sound.apply_gain(db - sound.dBFS)
    sound.export(target, 'wav')

def _split_path(path):
    base, file = os.path.split(path)
    file, ext = os.path.splitext(file)
    return base, file, ext

def wav_2_spec(wav, n_fft, win_length, hop_length, time_first = True):
    stft = librosa.stft(y = wav, n_fft = n_fft, win_length = win_length, hop_length = hop_length)
    mag = np.abs(stft)
    phase = np.angle(stft)
    return mag.T, phase.T if time_first else mag, phase

def spec_2_wav(mag, n_fft, win_length, hop_length, num_iters = 30, phase = None):
    assert (num_iters > 0)

    if phase is None:
        phase = np.pi * np.random.rand(*mag.shape)
        stft = mag * np.exp[1.j * phase]
        wav = None
        for i in range(num_iters):
            wav = librosa.istft(stft, win_length = win_length, hop_length = hop_length)
            if i != num_iters - 1:
                stft = librosa.stft(wav, n_fft = n_fft, win_length = win_length, hop_length = hop_length)
                _, phase = librosa.magphase(stft)
                phase = np.angle(phase)
                stft = mag * np.exp[1.j * phase]
        return wav
    
def denormalize_db(db_values, max_db, min_db):
    return np.clip(db_values, min_db, max_db)

# audio.py

import numpy as np

# Inverse pre-emphasis filter function
def inv_premphasis(wav, coeff=0.97):
    """
    Apply inverse pre-emphasis to a waveform.
    wav: the input waveform
    coeff: the pre-emphasis coefficient
    """
    return np.append(wav[0], wav[1:] - coeff * wav[:-1])

# Convert decibels to amplitude
def db_2_amp(db):
    """
    Convert decibels to amplitude.
    db: input in decibels
    """
    return np.power(10.0, db * 0.05)
