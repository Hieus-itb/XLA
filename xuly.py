import cv2
import numpy as np
import matplotlib.pyplot as plt


def count_objects(image_path):
    """
    Hàm đếm số vật thể trong ảnh
    """
    # 1. Đọc ảnh
    img = cv2.imread(image_path)
    if img is None:
        print("Không thể đọc ảnh!")
        return

    # 2. Chuyển sang ảnh xám
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 3. Làm mờ để giảm nhiễu
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # 4. Ngưỡng hóa (thresholding)
    # Có thể thử các phương pháp khác nhau:
    # - THRESH_BINARY: ngưỡng cố định
    # - THRESH_OTSU: tự động tìm ngưỡng tối ưu
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # 5. Morphological operations để làm sạch
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)

    # 6. Tìm contours (đường viền)
    contours, _ = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 7. Lọc contours theo diện tích (loại bỏ nhiễu nhỏ)
    min_area = 100  # Diện tích tối thiểu (có thể điều chỉnh)
    valid_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]

    # 8. Vẽ kết quả
    result = img.copy()
    for i, contour in enumerate(valid_contours):
        # Vẽ contour
        cv2.drawContours(result, [contour], -1, (0, 255, 0), 2)

        # Tính tâm của vật thể
        M = cv2.moments(contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            # Đánh số thứ tự
            cv2.putText(result, str(i + 1), (cx - 10, cy + 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # Hiển thị số lượng
    count = len(valid_contours)
    cv2.putText(result, f'So luong: {count}', (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # 9. Hiển thị các bước xử lý
    plt.figure(figsize=(15, 10))

    plt.subplot(2, 3, 1)
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title('Anh goc')
    plt.axis('off')

    plt.subplot(2, 3, 2)
    plt.imshow(gray, cmap='gray')
    plt.title('Anh xam')
    plt.axis('off')

    plt.subplot(2, 3, 3)
    plt.imshow(blurred, cmap='gray')
    plt.title('Lam mo')
    plt.axis('off')

    plt.subplot(2, 3, 4)
    plt.imshow(thresh, cmap='gray')
    plt.title('Nguong hoa')
    plt.axis('off')

    plt.subplot(2, 3, 5)
    plt.imshow(opening, cmap='gray')
    plt.title('Sau khi lam sach')
    plt.axis('off')

    plt.subplot(2, 3, 6)
    plt.imshow(cv2.cvtColor(result, cv2.COLOR_BGR2RGB))
    plt.title(f'Ket qua: {count} vat the')
    plt.axis('off')

    plt.tight_layout()
    plt.show()

    print(f"\nĐã phát hiện {count} vật thể!")
    return count, result


# Cách sử dụng:
if __name__ == "__main__":
    # Thay đổi đường dẫn ảnh của bạn
    image_path = "test_image.jpg"

    count, result_image = count_objects(image_path)

    # Lưu kết quả
    cv2.imwrite("result.jpg", result_image)