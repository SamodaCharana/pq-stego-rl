# src/metrics.py
import numpy as np
from skimage.metrics import peak_signal_noise_ratio as psnr, structural_similarity as ssim

def image_psnr_ssim(orig_arr, stego_arr):
    p = psnr(orig_arr, stego_arr, data_range=orig_arr.max()-orig_arr.min())
    s = ssim(orig_arr, stego_arr, multichannel=True)
    return p, s

def audio_snr(orig, stego):
    noise = orig - stego
    return 10.0 * np.log10((orig**2).mean() / (noise**2).mean() + 1e-12)
