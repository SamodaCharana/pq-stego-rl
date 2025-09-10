# src/stego_image.py
from PIL import Image
import numpy as np

def bytes_to_bitarray(b):
    return np.unpackbits(np.frombuffer(b, dtype=np.uint8))

def bitarray_to_bytes(bits):
    arr = np.packbits(bits)
    return arr.tobytes()

def embed_image_lsb(image_path, out_path, payload_bytes):
    im = Image.open(image_path).convert("RGB")
    arr = np.array(im)
    h,w,_ = arr.shape
    capacity = h*w*3  # bits
    bits = bytes_to_bitarray(payload_bytes)
    if bits.size > capacity:
        raise ValueError("payload too large")
    flat = arr.flatten()
    # set least-significant bit
    flat[:bits.size] = (flat[:bits.size] & ~1) | bits
    arr2 = flat.reshape(arr.shape)
    Image.fromarray(arr2).save(out_path, "PNG")
    return out_path

def extract_image_lsb(stego_path, payload_len_bytes):
    im = Image.open(stego_path).convert("RGB")
    arr = np.array(im).flatten()
    nbits = payload_len_bytes * 8
    bits = arr[:nbits] & 1
    return bitarray_to_bytes(bits)
