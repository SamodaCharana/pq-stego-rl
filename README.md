# PQC + RL Steganography

This project combines **Post-Quantum Cryptography (PQC)** with **Reinforcement Learning (RL)** based multi-layer steganography.

- **Kyber** → Key Encapsulation (KEM) for hybrid encryption  
- **Dilithium** → Digital signatures  
- **AES-GCM** → Symmetric encryption using shared secret from Kyber  
- **Steganography** → Embed ciphertext fragments in image/audio  
- **RL Agent** → Learn optimal fragmentation and allocation strategy  

---

## 1. Requirements

### System packages
Run once on Ubuntu/Debian:
```bash
sudo apt update
sudo apt install -y build-essential cmake ninja-build git ffmpeg \
    libsndfile1-dev libssl-dev python3-full python3-venv


# pq-stego-rl
