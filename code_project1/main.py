import tkinter as tk
from tkinter import filedialog, ttk
import cv2
from PIL import Image, ImageTk
import numpy as np

from image_ops import ImageContrast, ImageRestoration


class ModernStyle:
    """Custom modern theme for Tkinter"""
    @staticmethod
    def apply(style: ttk.Style):
        style.theme_use("default")

        # Global font
        style.configure(".", font=("Segoe UI", 10))

        # Modern buttons
        style.configure(
            "Modern.TButton",
            font=("Segoe UI", 11, "bold"),
            foreground="#ffffff",
            background="#4A6CF7",
            padding=8,
            relief="flat",
            borderwidth=0
        )

        style.map(
            "Modern.TButton",
            background=[("active", "#334DB3")]
        )


class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing App")
        self.root.geometry("1250x750")
        self.root.configure(bg="#DDE3FF")

        self.original_image = None
        self.processed_image = None

        # Apply custom theme
        style = ttk.Style()
        ModernStyle.apply(style)

        self.create_widgets()

    # ======== GUI BUILDING ==========
    def create_widgets(self):

        # ===== MAIN SCROLLABLE AREA =====
        container = tk.Frame(self.root)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container, bg="#DDE3FF", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        canvas.configure(yscrollcommand=scrollbar.set)

        # CONTENT FRAME
        content = tk.Frame(canvas, bg="#DDE3FF")

        # Buat window ID (supaya bisa di-resize)
        window_id = canvas.create_window((0, 0), window=content, anchor="nw")

        # UPDATE SCROLL REGION SETIAP KALI CANVAS BERUBAH
        def resize_frame(event):
            canvas.itemconfig(window_id, width=event.width)
            canvas.configure(scrollregion=canvas.bbox("all"))

        canvas.bind("<Configure>", resize_frame)

        # ===== TOP NAVBAR =====
        navbar = tk.Frame(content, bg="#2B2D42", height=60)
        navbar.pack(fill="x")

        title = tk.Label(
            navbar,
            text="✨ Image Processing App",
            bg="#2B2D42",
            fg="white",
            font=("Segoe UI", 16, "bold")
        )
        title.pack(pady=10)

        # ===== IMAGE SECTION =====
        self.display_frame = tk.Frame(content, bg="#DDE3FF")
        self.display_frame.pack(pady=20)

        card_style = {"bg": "white", "bd": 0, "highlightthickness": 0, "padx": 20, "pady": 20}

        # BEFORE
        before_card = tk.Frame(self.display_frame, **card_style)
        before_card.grid(row=0, column=0, padx=30)

        tk.Label(before_card, text="Before (Original)", font=("Segoe UI", 12, "bold"), bg="white").pack(pady=(0, 10))
        self.before = tk.Label(before_card, bg="white")
        self.before.pack()

        # AFTER
        after_card = tk.Frame(self.display_frame, **card_style)
        after_card.grid(row=0, column=1, padx=30)

        tk.Label(after_card, text="After (Processed)", font=("Segoe UI", 12, "bold"), bg="white").pack(pady=(0, 10))
        self.after = tk.Label(after_card, bg="white")
        self.after.pack()

        # LABEL HASIL EFek
        self.result_label = tk.Label(after_card, text="", bg="white", fg="#2B2D42",
                                    font=("Segoe UI", 11, "italic"))
        self.result_label.pack(pady=(10, 0))
        # ===== MENU GROUP =====
        menu_area = tk.Frame(content, bg="#DDE3FF")
        menu_area.pack(pady=30)

        group_card = lambda parent: tk.Frame(parent, bg="white", padx=20, pady=20, bd=1, relief="solid")

        # FILE GROUP
        file_group = group_card(menu_area)
        file_group.grid(row=0, column=0, padx=20, pady=10, sticky="nw")

        tk.Label(file_group, text="📁 File", bg="white", font=("Segoe UI", 12, "bold")).pack(pady=(0, 10))
        ttk.Button(file_group, text="📂 Buka", command=self.open_image, style="Modern.TButton").pack(fill="x", pady=5)
        ttk.Button(file_group, text="💾 Simpan", command=self.save_image, style="Modern.TButton").pack(fill="x", pady=5)

        # ENHANCEMENT
        enhance_group = group_card(menu_area)
        enhance_group.grid(row=0, column=1, padx=20, pady=10, sticky="nw")

        tk.Label(enhance_group, text="Enhancement", bg="white", font=("Segoe UI", 12, "bold")).pack(pady=(0, 10))
        ttk.Button(enhance_group, text="Contrast Stretch", command=self.apply_contrast, style="Modern.TButton").pack(fill="x", pady=5)
        ttk.Button(enhance_group, text="Gamma Correction", command=self.apply_gamma, style="Modern.TButton").pack(fill="x", pady=5)
        ttk.Button(enhance_group, text="Histogram Equalization", command=self.apply_hist_eq, style="Modern.TButton").pack(fill="x", pady=5)


        # RESTORATION
        restore_group = group_card(menu_area)
        restore_group.grid(row=0, column=2, padx=20, pady=10, sticky="nw")

        tk.Label(restore_group, text="Image Restoration", bg="white", font=("Segoe UI", 12, "bold")).pack(pady=(0, 10))
        ttk.Button(restore_group, text="Butter Worth", command=self.apply_butterworth, style="Modern.TButton").pack(fill="x", pady=5)
        ttk.Button(restore_group, text="Median Filter", command=self.apply_median, style="Modern.TButton").pack(fill="x", pady=5)
        ttk.Button(restore_group, text="Wiener Filter", command=self.apply_wiener, style="Modern.TButton").pack(fill="x", pady=5)

        # COLOR PROCESSING
        color_group = group_card(menu_area)
        color_group.grid(row=1, column=0, padx=20, pady=10, sticky="nw")




    # ========= IMAGE OPS (same as before) ==========
    def open_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("Image Files", "*.jpg *.png *.jpeg *.bmp *.tiff")]
        )
        if path:
            self.original_image = cv2.imread(path)
            self.processed_image = None
            self.show(self.original_image, self.before)
            self.after.config(image="")
            self.result_label.config(text="")


    def resize_image(self, img):
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        h, w = img_rgb.shape[:2]

        max_w = 250
        max_h = 250

        scale_w = max_w / w
        scale_h = max_h / h

        scale = min(scale_w, scale_h, 1)  # jangan perbesar gambar kecil

        new_w = int(w * scale)
        new_h = int(h * scale)

        img_rgb = cv2.resize(img_rgb, (new_w, new_h))
        return ImageTk.PhotoImage(Image.fromarray(img_rgb))

    def set_result_text(self, text):
        self.result_label.config(text=f"Hasil: {text}")

    def show(self, img, panel):
        img_tk = self.resize_image(img)
        panel.config(image=img_tk)
        panel.image = img_tk

    # ======= PROCESSING ==========
    def apply_contrast(self):
        if self.original_image is not None:
            self.processed_image = ImageContrast.contrast_stretch(self.original_image)
            self.show(self.processed_image, self.after)
            self.set_result_text("Contrast Stretch")


    def apply_butterworth(self):
        if self.original_image is not None:
            self.processed_image = ImageRestoration.butterworth_lowpass(self.original_image)
            self.show(self.processed_image, self.after)
            self.set_result_text("Butterworth Low-pass Filter")


    def apply_median(self):
        if self.original_image is not None:
            self.processed_image = ImageRestoration.median_filter(self.original_image)
            self.show(self.processed_image, self.after)
            self.set_result_text("Median Filter")


    def apply_wiener(self):
        if self.original_image is not None:
            self.processed_image = ImageRestoration.wiener_filter(self.original_image)
            self.show(self.processed_image, self.after)
            self.set_result_text("Wiener Filter")

    def apply_gamma(self):
        if self.original_image is not None:
            # gamma default = 1.5 (lebih terang)
            self.processed_image = ImageContrast.gamma_correction(self.original_image, gamma=1.5)
            self.show(self.processed_image, self.after)
            self.set_result_text("Gamma Correction (γ=1.5)")

    def apply_hist_eq(self):
        if self.original_image is not None:
            self.processed_image = ImageContrast.histogram_equalization(self.original_image)
            self.show(self.processed_image, self.after)
            self.set_result_text("Histogram Equalization")



    def apply_channel(self, channel):
        if self.original_image is not None:
            ch = ColorProcessing.extract_channel(self.original_image, channel)
            self.processed_image = cv2.cvtColor(ch, cv2.COLOR_GRAY2BGR)
            self.show(self.processed_image, self.after)

    def save_image(self):
        if self.processed_image is not None:
            path = filedialog.asksaveasfilename(defaultextension=".jpg")
            cv2.imwrite(path, self.processed_image)


if __name__ == "__main__":
    root = tk.Tk()
    ImageProcessingApp(root)
    root.mainloop()
