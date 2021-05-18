# API
Facebook Marketing API

## Hướng dẫn:

### 1. Cài đặt môi trường:

1. ✌ Windows

```sh
# 🗻 Tạo môi trường
python -m venv env
.\env\Scripts\activate

# ⚙ Cài đặt thư viện
pip install -r .\requirements.txt
```

2.  🐧 Linux

```sh
# 🗻 Tạo môi trường
python3 -m venv env
source env/bin/activate

# ⚙ Cài đặt thư viện
pip3 install -r .\requirements.txt
```
### 2. Nhập thông tin:

```sh
Nhập thông tin tại thư mục: INPUT

- File input_id_token.csv gồm: ACCOUNT_ID, ACCESS_TOKEN
    + ACCOUNT_ID: ID của tài khoản quảng cáo.
    + ACCESS_TOKEN: token truy cập.
> Mỗi thông tin nhập cách nhau một dấu phẩy, có thể nhập nhiều tài khoản vào danh sách.

- File input_field_time.txt gồm: TIME_SLEEP, GENERAL, ACTION
    + TIME_SLEEP: thời gian đợi giữa các lần update dữ liệu (giây).
    + GENERAL: điền vào các general-field cần truy xuất.
    + ACTION: điền vào các action-field cần truy xuất.
```
### 3. Khởi chạy và dừng chương trình:

- Chạy chương trình: 
```sh
# windows
python .\main.py

# linux 
python3 .\main.py
```
- Dừng chương trình: Ctrl + C

### 4. Xem kết quả:

Xem kết quả tại thư mục OUTPUT.



