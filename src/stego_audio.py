# src/stego_audio.py
import soundfile as sf
import numpy as np

def embed_audio_lsb(wav_in, wav_out, payload_bytes):
    data, sr = sf.read(wav_in, dtype='int16')
    flat = data.flatten()
    bits = np.unpackbits(np.frombuffer(payload_bytes, dtype=np.uint8))
    if bits.size > flat.size:
        raise ValueError("payload too large")
    flat[:bits.size] = (flat[:bits.size] & ~1) | bits
    data_out = flat.reshape(data.shape)
    sf.write(wav_out, data_out, sr, subtype='PCM_16')
    return wav_out

def extract_audio_lsb(wav_in, payload_len_bytes):
    data, sr = sf.read(wav_in, dtype='int16')
    flat = data.flatten()
    nbits = payload_len_bytes * 8
    bits = flat[:nbits] & 1
    return np.packbits(bits).tobytes()
