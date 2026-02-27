# Telegram Music Bot

Mục tiêu: bot Telegram tìm nhạc YouTube, trích xuất audio, tải video TikTok, upload lên Facebook Page và kiểm tra thông tin hệ thống.

## Yêu cầu
- Python 3.10+ (khuyên nghị 3.11)
- ffmpeg đã được cài đặt trên máy chủ
- Docker (tùy chọn, để sử dụng tính năng /sys kiểm tra containers)
- Supervisor (tùy chọn, để sử dụng tính năng /sys kiểm tra programs)

## Cài đặt môi trường (venv)
1) Tạo và cài dependencies:

```bash
./setup_venv.sh
```

2) Kích hoạt venv:

```bash
source .venv/bin/activate
```

3) Tạo file .env:

```bash
cp .env.example .env
```

Sau đó mở file .env và điền BOT_TOKEN của bạn.
Nếu muốn dùng /upfb, cần thêm FB_PAGE_ID và FB_PAGE_ACCESS_TOKEN.

## Chạy bot

```bash
python main.py
```

## Các lệnh có sẵn
- /start - Khởi động bot
- /help - Hiển thị hướng dẫn
- /search <tên bài hát> - Tìm và tải nhạc YouTube (MP3)
- /dowtiktok <URL> - Tải video TikTok
- /upfb <URL...> - Tải TikTok và upload lên Facebook Page
- /sys - Kiểm tra thông tin hệ thống (CPU, RAM, Disk, Docker, Supervisor)

## Ghi chú
- Nếu chưa có ffmpeg: cài đặt theo hệ điều hành (apt/brew/yum).
- Giới hạn thời lượng: YouTube < 30 phút, TikTok < 10 phút.
- /upfb chỉ hỗ trợ TikTok và cần Facebook Graph API token.
- /sys hiển thị thông tin hệ thống, Docker containers và Supervisor programs.

## Phụ thuộc
Xem [requirements.txt](requirements.txt).
