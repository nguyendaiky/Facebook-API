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

Nhập thông tin đầu vào tại: INPUT/input.csv

Gồm 3 trường: ACCOUNT_ID, ACCESS_TOKEN, SLEEP_TIME

- ACCOUNT_ID: ID của tài khoản quảng cáo.
- ACCESS_TOKEN: token truy cập.
- SLEEP_TIME: thời gian chờ update (giây).
> Mỗi thông tin nhập cách nhau một dấu phẩy, có thể nhập nhiều tài khoản.

### 3. Khởi chạy và dừng chương trình:

- Chạy chương trình: 
```sh
# windows
python .\main.py

# linux 
python3 .\main.py
```
- Dừng chương trình: Ctrl + C


