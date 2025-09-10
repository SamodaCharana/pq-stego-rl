# utils.py
import oqs
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import numpy as np


# --- Post-Quantum Encryption (Kyber) ---

def pq_encrypt(message: bytes):
    with oqs.KeyEncapsulation("Kyber512") as kem:
        secret_key = kem.generate_keypair()  # only one bytes object
        ciphertext, shared_secret = kem.encap_secret(secret_key)  # encrypt using the key
        public_key = secret_key  # in this version, public_key = secret_key
        return ciphertext, shared_secret, secret_key, public_key

def pq_decrypt(ciphertext: bytes, secret_key: bytes):
    with oqs.KeyEncapsulation("Kyber512") as kem:
        shared_secret = kem.decap_secret(ciphertext, secret_key)
        return shared_secret







# --- AES Encryption (Optional for message payload) ---
def aes_encrypt(message: bytes, key: bytes):
    """
    AES-GCM encrypt a message with the first 32 bytes of the key.
    Returns: nonce, ciphertext
    """
    aesgcm = AESGCM(key[:32])
    nonce = np.random.bytes(12)
    ct = aesgcm.encrypt(nonce, message, None)
    return nonce, ct

def aes_decrypt(ciphertext: bytes, key: bytes, nonce: bytes):
    """
    AES-GCM decrypt a ciphertext with the given key and nonce.
    Returns: plaintext message
    """
    aesgcm = AESGCM(key[:32])
    return aesgcm.decrypt(nonce, ciphertext, None)

# --- Fragmentation ---
def split_chunks(data: bytes, chunk_size: int):
    """
    Split bytes into fixed-size chunks.
    Returns: list of byte chunks
    """
    return [data[i:i+chunk_size] for i in range(0, len(data), chunk_size)]

def recombine_chunks(chunks: list):
    """
    Recombine a list of byte chunks into original bytes.
    """
    return b''.join(chunks)

# --- RL allocation placeholder ---
def rl_allocate_chunks(chunks: list, image_paths: list, audio_paths: list):
    """
    Placeholder RL agent to allocate chunks to images/audio.
    Currently performs round-robin allocation.
    Returns: list of tuples (chunk, carrier_path)
    """
    allocation = []
    media_paths = image_paths + audio_paths
    for i, chunk in enumerate(chunks):
        path = media_paths[i % len(media_paths)]
        allocation.append((chunk, path))
    return allocation
