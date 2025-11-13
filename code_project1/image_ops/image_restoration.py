import cv2
import numpy as np

class ImageRestoration:

    # ------------------------------------------------------
    # 1. BUTTERWORTH LOW-PASS FILTER (SMOOTHING)
    # ------------------------------------------------------
    @staticmethod
    def butterworth_lowpass(img, cutoff=30, order=2):
        # convert to grayscale terlebih dahulu
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # FFT
        dft = np.fft.fft2(gray)
        dft_shift = np.fft.fftshift(dft)

        rows, cols = gray.shape
        crow, ccol = rows // 2, cols // 2

        # Butterworth LPF Mask
        mask = np.zeros((rows, cols), np.float32)
        for u in range(rows):
            for v in range(cols):
                D = np.sqrt((u - crow)**2 + (v - ccol)**2)
                mask[u, v] = 1 / (1 + (D/cutoff)**(2*order))

        filtered = dft_shift * mask

        # Inverse FFT
        f_ishift = np.fft.ifftshift(filtered)
        img_back = np.fft.ifft2(f_ishift)
        img_back = np.abs(img_back)

        # kembalikan ke 3 channel
        result = cv2.cvtColor(img_back.astype(np.uint8), cv2.COLOR_GRAY2BGR)
        return result

    # ------------------------------------------------------
    # 2. WIENER FILTER (APROX) UNTUK DE-NOISING
    # ------------------------------------------------------
    @staticmethod
    def wiener_filter(img, kernel_size=5, noise_power=0.01):
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Kernel blur
        kernel = np.ones((kernel_size, kernel_size)) / (kernel_size**2)

        # FFT citra & kernel
        I = np.fft.fft2(img_gray)
        H = np.fft.fft2(kernel, s=img_gray.shape)

        # |H|^2
        H_conj = np.conj(H)
        H_abs2 = np.abs(H)**2

        # Wiener Filter formula
        wiener = (H_conj / (H_abs2 + noise_power)) * I

        # inverse FFT
        result = np.fft.ifft2(wiener)
        result = np.abs(result).astype(np.uint8)

        # balikkan ke BGR
        return cv2.cvtColor(result, cv2.COLOR_GRAY2BGR)

    # ------------------------------------------------------
    # 3. Median Filter tetap dipertahankan
    # ------------------------------------------------------
    @staticmethod
    def median_filter(img):
        return cv2.medianBlur(img, 5)
