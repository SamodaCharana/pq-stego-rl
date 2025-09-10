# src/experiments.py

import os
import glob
import sys

from .utils import pq_encrypt, pq_decrypt, split_chunks, recombine_chunks, rl_allocate_chunks
from .stego_image import embed_image_lsb, extract_image_lsb
from .stego_audio import embed_audio_lsb, extract_audio_lsb

# --- Configuration ---
IMAGE_DIR = "../data/images"
AUDIO_DIR = "../data/audio"
PAYLOAD_CHUNK_SIZE = 16  # bytes per chunk

# --- Step 1: Input message ---
message = input("Enter your message: ").encode()

# --- Step 2: PQC encryption ---
ciphertext, shared_secret, secret_key, public_key = pq_encrypt(message)

# --- Step 3: Split ciphertext into chunks ---
chunks = split_chunks(ciphertext, PAYLOAD_CHUNK_SIZE)

# --- Step 4: Load carrier files ---
image_files = glob.glob(os.path.join(IMAGE_DIR, "*.png"))
audio_files = glob.glob(os.path.join(AUDIO_DIR, "*.wav"))

# --- Step 5: Check for available carrier files ---
if not image_files and not audio_files:
    print("Error: No image or audio files found in the carrier directories.")
    sys.exit(1)

if not image_files:
    print("Warning: No image files found. Only audio files will be used.")
if not audio_files:
    print("Warning: No audio files found. Only image files will be used.")

# --- Step 6: Allocate chunks using RL (round-robin placeholder) ---
allocation = rl_allocate_chunks(chunks, image_files, audio_files)

# --- Step 7: Embed chunks ---
stego_image_paths = []
stego_audio_paths = []

for chunk, carrier_path in allocation:
    if carrier_path.endswith(".png"):
        out_path = carrier_path.replace(".png", "_stego.png")
        embed_image_lsb(carrier_path, out_path, chunk)
        stego_image_paths.append(out_path)
    elif carrier_path.endswith(".wav"):
        out_path = carrier_path.replace(".wav", "_stego.wav")
        embed_audio_lsb(carrier_path, out_path, chunk)
        stego_audio_paths.append(out_path)

print("\nChunks embedded into images and audio successfully.")

# --- Step 8: Extract and recombine chunks ---
extracted_chunks = []

for path in stego_image_paths:
    extracted_chunks.append(extract_image_lsb(path, PAYLOAD_CHUNK_SIZE))

for path in stego_audio_paths:
    extracted_chunks.append(extract_audio_lsb(path, PAYLOAD_CHUNK_SIZE))

recovered_ciphertext = recombine_chunks(extracted_chunks)

# --- Step 9: PQC decryption ---
recovered_message = pq_decrypt(recovered_ciphertext, secret_key)

print("\nOriginal message:", message.decode())
print("Recovered message:", recovered_message.decode())
