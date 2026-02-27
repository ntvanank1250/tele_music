# 🎵 Python Telegram Music Bot - Project Instructions

---

## 1️⃣ Mục tiêu (Core Objective)

Xây dựng Telegram Bot bằng Python cho phép người dùng:

- 🎧 **Tìm kiếm nhạc từ YouTube**: Trích xuất âm thanh và gửi file `.mp3` trực tiếp
- 🎬 **Tải video TikTok**: Gửi file video cho người dùng
- 🖥️ **Kiểm tra hệ thống**: Theo dõi Docker containers và Supervisor programs

---

## 2️⃣ Công nghệ yêu cầu (Tech Stack)

### Thư viện Python

- **Framework**: `python-telegram-bot` (version 20.x+, hỗ trợ asyncio)
- **Tìm kiếm**: `youtube-search-python` hoặc `yt-search`
- **Xử lý Audio/Video**: `yt-dlp` (Công cụ mạnh mẽ và cập nhật nhất)
- **Impersonation**: `curl-cffi` (Bypass bảo vệ anti-bot cho TikTok)
- **System Monitoring**: `psutil` (Thu thập thông tin CPU, RAM, Disk)
- **Environment**: `python-dotenv` (Quản lý biến môi trường)

### Yêu cầu hệ thống

- ✅ **ffmpeg**: Cài đặt sẵn để convert audio
- ✅ **Build tools**: gcc, g++, make
- ✅ **libcurl-dev**: Để build curl-cffi
- 🔧 **Docker** (tùy chọn): Để lệnh `/sys` hiển thị thông tin containers
- 🔧 **Supervisor** (tùy chọn): Để lệnh `/sys` hiển thị thông tin programs

---

## 3️⃣ Cấu trúc Logic (Flow Logic)

### 3.1. 🚀 Lệnh `/start`

- Hiển thị thông báo chào mừng
- Hướng dẫn cơ bản cho người dùng mới

### 3.2. 📖 Lệnh `/help`

Hiển thị menu đầy đủ với:
- Danh sách các lệnh có sẵn
- Hướng dẫn sử dụng từng chức năng
- Lưu ý và giới hạn
- Mẹo sử dụng

### 3.3. 🎵 Lệnh `/search [tên bài hát]`

**Flow:**
1. Bot gọi `VideosSearch` để lấy 5 kết quả hàng đầu
2. Trả về tin nhắn kèm `InlineKeyboardMarkup`
3. Mỗi nút chứa `callback_data` là ID của video

**Xử lý Callback (Khi bấm nút):**
1. Hiển thị thông báo *"Đang xử lý âm thanh... 🎧"*
2. Sử dụng `yt-dlp` với `postprocessors` để trích xuất audio `.mp3`
3. Gửi file qua `context.bot.send_audio`

**⚠️ Giới hạn:** Chỉ tải các bài < 30 phút

### 3.4. 🎬 Lệnh `/dowtiktok [URL]`

**Flow:**
1. Nhận URL video TikTok từ người dùng
2. Validate URL (phải chứa `tiktok.com` hoặc `vm.tiktok.com`)
3. Hiển thị thông báo *"Đang tải video TikTok... 🎬"*
4. Sử dụng `yt-dlp` để tải video (format: best)
5. Gửi file qua `context.bot.send_video`

**⚠️ Giới hạn:** Chỉ tải video < 10 phút

### 3.5. 📤 Lệnh `/upfb [URL...]`

**Flow:**
1. Nhận 1 hoặc nhiều URL TikTok từ người dùng
2. Validate URL (phải chứa `tiktok.com` hoặc `vm.tiktok.com`)
3. Tải video TikTok bằng `yt-dlp`
4. Upload lên Facebook Page qua Graph API

**🔑 Yêu cầu ENV:**
- `FB_PAGE_ID`
- `FB_PAGE_ACCESS_TOKEN`

**⚠️ Giới hạn:** Chỉ tải video < 10 phút

### 3.6. 🖥️ Lệnh `/sys`

Hiển thị thông tin hệ thống chi tiết:

**🔹 Thông tin OS:**
- Platform, Architecture, System version

**🔹 Tài nguyên hệ thống (qua `psutil`):**
- **CPU**: Số cores và % sử dụng
- **RAM**: Used/Total và phần trăm
- **Disk**: Used/Total và phần trăm

**🔹 Docker (nếu có):**
- Tổng số containers và số đang chạy
- Danh sách containers đang chạy (name, image, status)
- Danh sách containers đã dừng

**🔹 Supervisor (nếu có):**
- Tổng số programs và số đang chạy
- Danh sách programs đang chạy (name, uptime)
- Danh sách programs đã dừng

**🛠️ Kỹ thuật:**
- Sử dụng `asyncio.create_subprocess_exec` để chạy:
  - `docker ps` (với và không có `-a` flag)
  - `supervisorctl status`
- Format output dạng Markdown với emoji

### 3.7. 🗑️ Tối ưu hóa bộ nhớ

**Áp dụng cho tất cả download (YouTube và TikTok):**
- Sử dụng `tempfile.mkdtemp()` để tạo thư mục tạm
- Xóa file tạm sau khi gửi thành công
- Cleanup trong `finally` block để đảm bảo luôn xóa file

---

## 4️⃣ Quy tắc lập trình (Coding Rules)

### ⚡ Asynchronous
- **PHẢI** sử dụng `async`/`await` để bot không bị treo khi có nhiều người dùng

### 🛡️ Error Handling
- Bắt lỗi `DownloadError` từ `yt-dlp` (video bị chặn, giới hạn độ tuổi)
- Handle gracefully và thông báo rõ ràng cho user

### 📝 Logging
- Sử dụng module `logging` của Python
- Theo dõi tiến trình và debug lỗi

### 🔐 Environment Variables
- Lưu `BOT_TOKEN` trong file `.env`
- Sử dụng `python-dotenv` để đọc
- Không commit `.env` vào git

### 🎯 Bot Commands Menu
- Sử dụng `set_my_commands()` để hiển thị menu lệnh
- Menu xuất hiện bên cạnh ô nhập tin nhắn trong Telegram

---

## 5️⃣ Cấu trúc File đề xuất

```
tele_music/
├── main.py                   # 🎯 Entry point
│   ├── Application setup
│   ├── Handlers registration
│   └── post_init() - Set bot commands menu
│
├── search_engine.py          # 🔍 YouTube search
│   └── search_youtube()
│
├── downloader.py             # 📥 Download logic
│   ├── download_audio_mp3()      # YouTube → MP3
│   └── download_tiktok_video()   # TikTok → Video
│
├── system_info.py            # 🖥️ System monitoring
│   ├── get_system_info()         # Tổng hợp tất cả info
│   ├── get_docker_info()         # Docker containers
│   ├── get_supervisor_info()     # Supervisor programs
│   └── _format_bytes()           # Helper function
│
├── facebook_uploader.py      # 📤 Facebook Graph API
│   └── upload_video_to_facebook()
│
├── requirements.txt          # 📦 Dependencies
├── .env                      # 🔐 Environment variables
└── README.md                 # 📖 Documentation
```

---

## 6️⃣ Các lệnh có sẵn (Available Commands)

| Lệnh | Mô tả |
|------|-------|
| `/start` | 🚀 Khởi động bot và hiển thị thông báo chào mừng |
| `/help` | 📖 Hiển thị menu trợ giúp đầy đủ |
| `/search <tên bài hát>` | 🎵 Tìm kiếm và tải nhạc từ YouTube (MP3) |
| `/dowtiktok <URL>` | 🎬 Tải video từ TikTok |
| `/upfb <URL...>` | 📤 Tải TikTok và upload lên Facebook Page |
| `/sys` | 🖥️ Kiểm tra thông tin hệ thống (CPU, RAM, Disk, Docker, Supervisor) |

---

## 7️⃣ Giới hạn và Lưu ý (Limits & Notes)

### ⏱️ Giới hạn thời lượng
- **YouTube**: < 30 phút → Output là MP3
- **TikTok**: < 10 phút → Output là video gốc

### ⚠️ Xử lý lỗi
- Video riêng tư, bị chặn, giới hạn độ tuổi không tải được
- Hiển thị thông báo rõ ràng cho người dùng

### 🔒 Permission Control
- Có thể giới hạn user qua `ALLOWED_TELEGRAM_IDS` trong `.env`
- Format: danh sách ID phân cách bằng dấu phẩy

### 📤 Facebook Upload
- **Yêu cầu**: `FB_PAGE_ID` và `FB_PAGE_ACCESS_TOKEN` (Graph API)
- Chỉ hỗ trợ upload video từ TikTok

---

**📌 Lưu ý:** File này là hướng dẫn chi tiết cho việc phát triển và maintain bot. Đọc kỹ trước khi code!