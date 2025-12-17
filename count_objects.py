import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog, ttk
from PIL import Image, ImageTk


class ObjectCounterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Ứng Dụng Đếm Vật Thể")
        self.root.geometry("1200x700")
        self.root.configure(bg='#f0f0f0')

        self.current_image = None
        self.result_image = None
        self.object_count = 0

        self.setup_ui()

    def setup_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        header_frame.pack(fill='x', pady=(0, 10))
        header_frame.pack_propagate(False)

        title_label = tk.Label(
            header_frame,
            text="ỨNG DỤNG ĐẾM VẬT THỂ",
            font=('Arial', 24, 'bold'),
            bg='#2c3e50',
            fg='white'
        )
        title_label.pack(pady=20)

        # Button chọn ảnh
        button_frame = tk.Frame(self.root, bg='#f0f0f0')
        button_frame.pack(pady=10)

        self.select_btn = tk.Button(
            button_frame,
            text="📁 Chọn Ảnh",
            command=self.select_image,
            font=('Arial', 14, 'bold'),
            bg='#3498db',
            fg='white',
            padx=30,
            pady=15,
            cursor='hand2',
            relief='flat',
            activebackground='#2980b9'
        )
        self.select_btn.pack(side='left', padx=10)

        self.process_btn = tk.Button(
            button_frame,
            text="⚙️ Xử Lý",
            command=self.process_image,
            font=('Arial', 14, 'bold'),
            bg='#27ae60',
            fg='white',
            padx=30,
            pady=15,
            cursor='hand2',
            relief='flat',
            state='disabled',
            activebackground='#229954'
        )
        self.process_btn.pack(side='left', padx=10)

        self.save_btn = tk.Button(
            button_frame,
            text="💾 Lưu Kết Quả",
            command=self.save_result,
            font=('Arial', 14, 'bold'),
            bg='#e67e22',
            fg='white',
            padx=30,
            pady=15,
            cursor='hand2',
            relief='flat',
            state='disabled',
            activebackground='#d35400'
        )
        self.save_btn.pack(side='left', padx=10)

        # Main container
        main_container = tk.Frame(self.root, bg='#f0f0f0')
        main_container.pack(fill='both', expand=True, padx=20, pady=10)

        # Left panel - Hiển thị ảnh
        left_panel = tk.Frame(main_container, bg='white', relief='solid', bd=2)
        left_panel.pack(side='left', fill='both', expand=True, padx=(0, 10))

        image_title = tk.Label(
            left_panel,
            text="ẢNH KẾT QUẢ",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        image_title.pack(pady=10)

        self.image_label = tk.Label(left_panel, bg='#ecf0f1', text="Chưa có ảnh", font=('Arial', 12), fg='#7f8c8d')
        self.image_label.pack(fill='both', expand=True, padx=10, pady=10)

        # Right panel - Thông tin
        right_panel = tk.Frame(main_container, bg='white', relief='solid', bd=2, width=350)
        right_panel.pack(side='right', fill='both', padx=(10, 0))
        right_panel.pack_propagate(False)

        info_title = tk.Label(
            right_panel,
            text="THÔNG TIN",
            font=('Arial', 16, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        info_title.pack(pady=15)

        # Số lượng vật thể
        count_frame = tk.Frame(right_panel, bg='#3498db', relief='flat')
        count_frame.pack(pady=20, padx=20, fill='x')

        count_label = tk.Label(
            count_frame,
            text="SỐ LƯỢNG VẬT THỂ",
            font=('Arial', 12, 'bold'),
            bg='#3498db',
            fg='white'
        )
        count_label.pack(pady=(15, 5))

        self.count_value = tk.Label(
            count_frame,
            text="0",
            font=('Arial', 48, 'bold'),
            bg='#3498db',
            fg='white'
        )
        self.count_value.pack(pady=(5, 15))

        # Thông tin chi tiết
        detail_frame = tk.Frame(right_panel, bg='white')
        detail_frame.pack(pady=20, padx=20, fill='both', expand=True)

        self.status_label = tk.Label(
            detail_frame,
            text="📌 Trạng thái: Chờ chọn ảnh",
            font=('Arial', 11),
            bg='white',
            fg='#7f8c8d',
            anchor='w',
            justify='left',
            wraplength=280
        )
        self.status_label.pack(anchor='w', pady=5)

        self.file_label = tk.Label(
            detail_frame,
            text="📄 File: Chưa có",
            font=('Arial', 11),
            bg='white',
            fg='#7f8c8d',
            anchor='w',
            justify='left',
            wraplength=280
        )
        self.file_label.pack(anchor='w', pady=5)

        # Hướng dẫn
        guide_frame = tk.LabelFrame(
            detail_frame,
            text="📖 Hướng Dẫn",
            font=('Arial', 11, 'bold'),
            bg='white',
            fg='#2c3e50'
        )
        guide_frame.pack(anchor='w', pady=20, fill='x')

        guide_text = """
1. Nhấn "Chọn Ảnh" để chọn file
2. Nhấn "Xử Lý" để đếm vật thể
3. Nhấn "Lưu Kết Quả" để lưu ảnh

💡 Lưu ý: Ảnh nên có nền
đơn giản và vật thể tách biệt
rõ ràng để kết quả tốt nhất.
        """

        guide_label = tk.Label(
            guide_frame,
            text=guide_text.strip(),
            font=('Arial', 10),
            bg='white',
            fg='#555555',
            justify='left',
            anchor='w'
        )
        guide_label.pack(padx=10, pady=10, anchor='w')

    def select_image(self):
        file_path = filedialog.askopenfilename(
            title="Chọn ảnh",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp"),
                ("All files", "*.*")
            ]
        )

        if file_path:
            self.current_image = cv2.imread(file_path)
            if self.current_image is not None:
                self.display_image(self.current_image)
                self.process_btn.config(state='normal')
                self.status_label.config(text="📌 Trạng thái: Đã chọn ảnh")
                self.file_label.config(text=f"📄 File: {file_path.split('/')[-1]}")
                self.count_value.config(text="0")
                self.save_btn.config(state='disabled')

    def process_image(self):
        if self.current_image is None:
            return

        self.status_label.config(text="📌 Trạng thái: Đang xử lý...")
        self.root.update()

        # Xử lý ảnh
        gray = cv2.cvtColor(self.current_image, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        kernel = np.ones((3, 3), np.uint8)
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

        contours, _ = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        min_area = 100
        valid_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]

        # Vẽ kết quả
        self.result_image = self.current_image.copy()
        for i, contour in enumerate(valid_contours):
            cv2.drawContours(self.result_image, [contour], -1, (0, 255, 0), 2)

            M = cv2.moments(contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                cv2.putText(self.result_image, str(i + 1), (cx - 10, cy + 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

        self.object_count = len(valid_contours)

        # Thêm text số lượng lên ảnh
        cv2.putText(self.result_image, f'So luong: {self.object_count}', (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

        # Hiển thị kết quả
        self.display_image(self.result_image)
        self.count_value.config(text=str(self.object_count))
        self.status_label.config(text="📌 Trạng thái: Đã xử lý xong!")
        self.save_btn.config(state='normal')

    def display_image(self, cv_image):
        # Chuyển đổi từ BGR sang RGB
        rgb_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)

        # Resize để fit vào label
        height, width = rgb_image.shape[:2]
        max_width = 700
        max_height = 500

        scale = min(max_width / width, max_height / height)
        new_width = int(width * scale)
        new_height = int(height * scale)

        resized = cv2.resize(rgb_image, (new_width, new_height))

        # Chuyển sang ImageTk
        img = Image.fromarray(resized)
        photo = ImageTk.PhotoImage(image=img)

        self.image_label.config(image=photo, text="")
        self.image_label.image = photo

    def save_result(self):
        if self.result_image is None:
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("All files", "*.*")]
        )

        if file_path:
            cv2.imwrite(file_path, self.result_image)
            self.status_label.config(text="📌 Trạng thái: Đã lưu kết quả!")


if __name__ == "__main__":
    root = tk.Tk()
    app = ObjectCounterApp(root)
    root.mainloop()