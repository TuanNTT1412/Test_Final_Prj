# Hướng dẫn sử dụng và giải thích mã nguồn

Tài liệu này hướng dẫn cách thiết lập, chạy hệ thống tiền xử lý ảnh và giao diện chụp ảnh (Test_Camera), đồng thời giải thích các công nghệ và file code.

## 1. Môi trường và công nghệ sử dụng

Dự án sử dụng Python để xử lý ảnh với các thư viện sau:
- **`opencv-python` (`cv2`)**: Dùng để đọc/ghi ảnh, chuyển đổi không gian màu (LAB), áp dụng cân bằng sáng (CLAHE), phân tích pixel và cắt ảnh.
- **`numpy`**: Hỗ trợ xử lý ma trận ảnh.
- **`rembg`**: Dùng để nhận diện và xóa nền ảnh.

Cài đặt các thư viện:
```bash
pip install opencv-python numpy rembg
```

## 2. Tiền xử lý ảnh so sánh (`preprocess_image.py`)

### Mục đích
Tiền xử lý hình ảnh để phục vụ cho việc so sánh và khớp đặc trưng (ví dụ dùng thuật toán SuperPoint).

### Cách chạy
1. Đặt 2 file ảnh cùng cấp thư mục với file code:
   - `anh_goc.jpg`
   - `anh_khach.jpg`
2. Chạy lệnh:
   ```bash
   python preprocess_image.py
   ```
3. Kết quả: Tạo ra 2 file `anh_goc_tien_xu_ly.jpg` và `anh_khach_tien_xu_ly.jpg`.

### Giải thích code
- **Bóc nền**: Dùng `rembg` để tách nền.
- **Cân bằng sáng**: Chuyển ảnh sang hệ màu LAB, áp dụng `CLAHE` lên kênh `L` (Lightness). Việc này giúp cân bằng độ sáng mà không làm sai lệch màu sắc thực (kênh A và B).
- **Tô đen nền**: Dùng kênh alpha từ bước bóc nền để xác định vùng nền và đổi màu vùng đó thành đen `[0, 0, 0]`. Điều này giúp chuẩn hóa đầu vào cho AI trích xuất đặc trưng.

## 3. Tiền xử lý ảnh chụp mẫu (`preprocess_gimage.py`)

### Mục đích
Chuẩn bị các ảnh mờ (ghost images) để làm lớp phủ hướng dẫn canh góc chụp trong thư mục `Test_Camera`.

### Cách chạy
1. Đặt 4 file ảnh cùng cấp thư mục với code:
   - `truoc.jpg`
   - `sau.jpg`
   - `trai.jpg`
   - `phai.jpg`
2. Chạy lệnh:
   ```bash
   python preprocess_gimage.py
   ```
3. Kết quả: Tạo ra 4 file PNG nền trong suốt: `truoc_nb.png`, `sau_nb.png`, `trai_nb.png`, `phai_nb.png`.

### Giải thích code
- **Xóa nền**: Dùng `rembg` để xóa nền.
- **Cắt sát viền**: Dùng `cv2.findNonZero` trên kênh alpha để tìm các pixel của vật thể, sau đó dùng `cv2.boundingRect` để lấy khung chữ nhật bao quanh vật thể.
- **Lưu ảnh**: Cắt ảnh theo khung vừa tìm được và lưu định dạng `.png` để giữ nền trong suốt và giảm kích thước file.

## 4. Chạy giao diện camera (`Test_Camera`)

Thư mục `Test_Camera` chứa code web để hiển thị giao diện chụp ảnh trên điện thoại, sử dụng ảnh mẫu (ghost images) làm lớp phủ.

### Các bước test:
1. Tạo 4 thư mục con `1`, `2`, `3`, `4` bên trong thư mục `Test_Camera`.
2. Copy 4 file `.png` được tạo từ `preprocess_gimage.py` vào chung một thư mục (ví dụ thư mục `1`). Lặp lại quá trình này cho các thư mục còn lại.
3. Upload toàn bộ thư mục `Test_Camera` lên các dịch vụ hosting như Netlify.
4. Mở link web trên điện thoại để kiểm tra giao diện chụp ảnh có lớp phủ.

### Quy trình thực tế
Khi triển khai thực tế:
- Quá trình tiền xử lý được thực hiện tự động trên cloud khi shop upload ảnh, và ghost image được lưu trên cloud.
- Khi người dùng cần hoàn tiền, hệ thống sẽ lấy đúng ghost image của sản phẩm đó để hiển thị trên trang chụp ảnh mà không cần tạo thư mục thủ công.
