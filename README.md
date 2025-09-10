# PQC + RL Steganography

A **Post-Quantum Cryptography (PQC) based steganography project** that hides encrypted messages into image and audio files using **Kyber** key encapsulation. The allocation of chunks to carrier files is done via a placeholder **reinforcement learning (RL)** approach (currently round-robin).

---

## Table of Contents

* [Project Overview](#project-overview)
* [Features](#features)
* [Directory Structure](#directory-structure)
* [Setup](#setup)
* [Usage](#usage)
* [Dependencies](#dependencies)
* [Post-Quantum Library Setup](#post-quantum-library-setup)
* [Notes](#notes)
* [License](#license)

---

## Project Overview

This project demonstrates how to:

1. Encrypt a secret message using a **post-quantum algorithm (Kyber512)**.
2. Split the encrypted message into chunks.
3. Embed chunks into image (`.png`) and audio (`.wav`) files.
4. Extract and recombine chunks from the carriers.
5. Decrypt the message to recover the original content.

This is useful for research on **secure communication in a post-quantum era**.

---

## Features

* **Post-Quantum Encryption**: Uses Kyber512 key encapsulation from liboqs.
* **AES Optional Encryption**: Additional symmetric encryption on the message payload.
* **Steganography**: Supports hiding data in both images and audio using LSB technique.
* **Chunk Allocation**: Placeholder RL allocation (currently round-robin) for distributing chunks among media files.
* **Recoverable**: Allows message recovery after extraction.

---

## Directory Structure

```
pq-stego-rl/
├── src/
│   ├── experiments.py        # Main experiment script
│   ├── utils.py              # Encryption, chunking, allocation functions
│   ├── stego_image.py        # Image LSB embedding/extraction
│   └── stego_audio.py        # Audio LSB embedding/extraction
├── data/
│   ├── images/               # Carrier image files (e.g., cover1.png)
│   └── audio/                # Carrier audio files (e.g., cover1.wav)
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

---

## Setup

1. **Clone the repository**

```bash
git clone <YOUR_GITHUB_REPO_URL>
cd pq-stego-rl
```

2. **Create and activate a virtual environment**

```bash
python3 -m venv venv
source venv/bin/activate
```

3. **Upgrade pip and install dependencies**

```bash
pip install -U pip setuptools wheel
pip install -r requirements.txt
```

4. **Install liboqs-python**

Liboqs-python cannot be installed via pip. Follow instructions here:
[https://openquantumsafe.org/liboqs/python/](https://openquantumsafe.org/liboqs/python/)

Verify that the `oqs` module works:

```bash
python3 -c "import oqs; print(dir(oqs))"
```

---

## Usage

Run the experiments script:

```bash
python3 -m src.experiments
```

* Enter the secret message when prompted.
* The script will:

  1. Encrypt the message using Kyber512.
  2. Split the ciphertext into 16-byte chunks.
  3. Embed the chunks into available images and audio files.
* After embedding, the script will extract and recombine the chunks and decrypt the message.
* You will see the original and recovered message printed.

---

## Dependencies

* `numpy==1.27.6`
* `cryptography==41.0.3`
* `liboqs-python` (must be built manually)

> **Note:** liboqs-python is required for post-quantum cryptography operations and cannot be installed via pip.

---

## Post-Quantum Library Setup

1. Clone and build liboqs-python:

```bash
git clone --recursive https://github.com/open-quantum-safe/liboqs-python.git
cd liboqs-python
python3 setup.py install
```

2. Verify installation:

```bash
python3 -c "import oqs; print(oqs.get_enabled_kems())"
```

---

## Notes

* Ensure `data/images` and `data/audio` folders contain carrier files. Minimum recommended: 5 images + 5 audio files.
* RL allocation is currently round-robin. You can replace it with a real RL agent for dynamic allocation.
* AES encryption is optional; currently, the project uses Kyber512 for message encryption.
* Make sure your Python virtual environment is active when running scripts.
* All experiments and scripts should be executed from the project root (`pq-stego-rl/`).

---

## License

**MIT License**
Feel free to use, modify, and distribute for research and educational purposes.
