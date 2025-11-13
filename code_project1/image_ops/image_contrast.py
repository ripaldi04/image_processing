import cv2
import numpy as np

class ImageContrast:

    # ------------------------------------------------------
    # 1. CONTRAST STRETCHING (MIN-MAX NORMALIZATION)
    # ------------------------------------------------------
    @staticmethod
    def contrast_stretch(img):
        img = img.astype(np.float32)
        for i in range(3):
            min_val = img[:, :, i].min()
            max_val = img[:, :, i].max()
            if max_val - min_val != 0:
                img[:, :, i] = (img[:, :, i] - min_val) / (max_val - min_val) * 255
        return img.astype(np.uint8)

    # ------------------------------------------------------
    # 2. GAMMA CORRECTION
    # ------------------------------------------------------
    @staticmethod
    def gamma_correction(img, gamma=1.0):
        # gamma < 1 -> lebih terang
        # gamma > 1 -> lebih gelap
        inv_gamma = 1.0 / gamma
        table = np.array([(i / 255.0) ** inv_gamma * 255
                          for i in np.arange(256)]).astype("uint8")
        return cv2.LUT(img, table)

    # ------------------------------------------------------
    # 3. HISTOGRAM EQUALIZATION (AUTO: GRAY OR COLOR)
    # ------------------------------------------------------
    @staticmethod
    def histogram_equalization(img):
        # Jika grayscale
        if len(img.shape) == 2:
            return cv2.equalizeHist(img)

        # Jika berwarna → convert ke YCrCb lalu equalize channel Y
        ycrcb = cv2.cvtColor(img, cv2.COLOR_BGR2YCrCb)
        y, cr, cb = cv2.split(ycrcb)

        y_eq = cv2.equalizeHist(y)

        ycrcb_eq = cv2.merge((y_eq, cr, cb))
        result = cv2.cvtColor(ycrcb_eq, cv2.COLOR_YCrCb2BGR)
        return result
