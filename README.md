# Hướng dẫn cài đặt
## 1. 1. Cài đặt các gói phần mềm
Trước tiên, cần cài đặt các gói phần mềm cần thiết cho dự án bằng cách chạy lệnh sau trong terminal:

```commandline
pip install -r requirements.txt
```
## 2. Cấu hình cơ sở dữ liệu
Tạo một file db_config.py trong thư mục gốc của dự án và điền thông tin cấu hình của cơ sở dữ liệu MySQL như sau:
```commandline
DATABASE_ENGINE = 'django.db.backends.mysql'
DATABASE_NAME = 'tên_cơ_sở_dữ_liệu'
DATABASE_USER = 'tên_người_dùng'
DATABASE_PASSWORD = 'mật_khẩu'
DATABASE_HOST = 'địa_chỉ_host'
DATABASE_PORT = 'cổng'
```
-   Lưu ý thay thế các giá trị tên_cơ_sở_dữ_liệu, tên_người_dùng, mật_khẩu, địa_chỉ_host và cổng bằng thông tin cụ thể của cơ sở dữ liệu MySQL bạn đang sử dụng.
-   Sử dụng dữ liệu trong file init_sql.sql để khởi tạo giá trị cho các quan hệ
## 3. Kết nối với cơ sở dữ liệu
```commandline
python manage.py migrate
```
## 4. Khởi động dự án
Cuối cùng, để khởi động dự án, chúng ta sử dụng lệnh sau:
```commandline
py manage.py runserver
```
Sau khi chạy lệnh này, bạn sẽ thấy dự án được khởi động trên địa chỉ mặc định của Django (thường là http://127.0.0.1:8000/).
## Chú ý
-   Đảm bảo rằng bạn đã cài đặt MySQL và có thông tin cấu hình chính xác của cơ sở dữ liệu trước khi thực hiện các bước trên.
-   Luôn giữ bảo mật thông tin cấu hình cơ sở dữ liệu bằng cách không chia sẻ file db_config.py với người khác.
