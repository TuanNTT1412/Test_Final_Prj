import cv2
import numpy as np
from rembg import remove
import os

def apply_clahe_lab(img):
    """Cân bằng độ sáng trong không gian màu LAB (tránh làm sai lệch màu thật)"""
    lab = cv2.cvtColor(img, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    l_eq = clahe.apply(l)
    
    fixed_lab = cv2.merge((l_eq, a, b))
    return cv2.cvtColor(fixed_lab, cv2.COLOR_LAB2BGR)

def preprocess_image(input_path, output_path):
    """
    Hàm tiền xử lý độc lập cho 1 bức ảnh.
    Bóc nền -> Cân bằng sáng -> Tô đen nền.
    """
    if not os.path.exists(input_path):
        print(f"❌ Lỗi: Không tìm thấy file ảnh tại '{input_path}'")
        return False

    img = cv2.imread(input_path)
    if img is None:
        print(f"❌ Lỗi: Không thể đọc dữ liệu ảnh '{input_path}' (file hỏng hoặc sai định dạng)")
        return False

    print(f"⏳ Đang xử lý: {input_path}...")
    
    # 1. Bóc tách phông nền bằng AI
    img_nobg = remove(img)
    alpha_channel = img_nobg[:, :, 3]
    img_bgr = img_nobg[:, :, 0:3].copy()
    
    # 2. Cân bằng sáng CLAHE
    img_bgr = apply_clahe_lab(img_bgr)
    
    # 3. Tô đen phần nền lộn xộn (chuẩn hóa ma trận cho SuperPoint)
    img_bgr[alpha_channel == 0] = [0, 0, 0] 

    # 4. Lưu kết quả ra ổ cứng
    cv2.imwrite(output_path, img_bgr)
    print(f"✅ Xong! Đã lưu ảnh tại: {output_path}")
    
    return True

if __name__ == "__main__":
    preprocess_image('anh_goc.jpg', 'anh_goc_tien_xu_ly.jpg')
    
    preprocess_image('anh_khach.jpg', 'anh_khach_tien_xu_ly.jpg')