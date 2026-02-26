Project Instructions: Python Telegram Music Bot
1. Mục tiêu (Core Objective)
Xây dựng Telegram Bot bằng Python cho phép người dùng:
- Tìm kiếm nhạc từ YouTube, trích xuất âm thanh và gửi file .mp3 trực tiếp.
- Tải video TikTok và gửi file video cho người dùng.

2. Công nghệ yêu cầu (Tech Stack)
Framework: python-telegram-bot (version 20.x trở lên, sử dụng asyncio).

Tìm kiếm: Youtube-python hoặc yt-search.

Xử lý Audio: yt-dlp (Công cụ mạnh mẽ và cập nhật nhất hiện nay).

Yêu cầu hệ thống: Máy chủ cần cài đặt sẵn ffmpeg để convert audio.

3. Cấu trúc Logic (Flow Logic)

3.1. Lệnh /start:
Hiển thị thông báo chào mừng và hướng dẫn cơ bản.

3.2. Lệnh /help:
Hiển thị menu đầy đủ với:
- Danh sách các lệnh có sẵn
- Hướng dẫn sử dụng từng chức năng
- Lưu ý và giới hạn
- Mẹo sử dụng

3.3. Lệnh /search [tên bài hát]:
Bot gọi VideosSearch để lấy 5 kết quả hàng đầu.

Trả về tin nhắn kèm InlineKeyboardMarkup. Mỗi nút chứa callback_data là ID của video.

Xử lý Callback (Khi bấm nút):

Hiển thị thông báo "Đang xử lý âm thanh... 🎧".

Sử dụng yt-dlp với option postprocessors để trích xuất audio định dạng .mp3.

Sử dụng context.bot.send_audio để gửi file.

Giới hạn: Chỉ tải các bài < 30 phút.

3.4. Lệnh /dowtiktok [URL]:
Nhận URL video TikTok từ người dùng.

Validate URL (phải chứa "tiktok.com" hoặc "vm.tiktok.com").

Hiển thị thông báo "Đang tải video TikTok... 🎬".

Sử dụng yt-dlp để tải video TikTok (format: best).

Sử dụng context.bot.send_video để gửi file video.

Giới hạn: Chỉ tải video < 10 phút.

3.5. Tối ưu hóa bộ nhớ (cho cả YouTube và TikTok):
Xóa file tạm sau khi gửi thành công để tránh đầy ổ cứng.

Sử dụng tempfile.mkdtemp để tạo thư mục tạm.

Cleanup trong finally block để đảm bảo luôn xóa file.

4. Quy tắc lập trình (Coding Rules)
Asynchronous: Phải sử dụng async/await để bot không bị treo khi có nhiều người dùng cùng lúc.

Error Handling: Bắt lỗi DownloadError từ yt-dlp (thường do video bị chặn hoặc giới hạn độ tuổi).

Logging: Sử dụng module logging của Python để theo dõi tiến trình.

Environment: Lưu BOT_TOKEN trong file .env và dùng python-dotenv để đọc.

Bot Commands Menu: Sử dụng set_my_commands để hiển thị menu lệnh trong Telegram (nút menu bên cạnh ô nhập tin nhắn).

5. Cấu trúc File đề xuất
main.py: Khởi tạo Application và đăng ký Handlers (start, help, search, dowtiktok).
  - post_init(): Callback để set bot commands menu sau khi bot khởi động
  - Sử dụng BotCommand để định nghĩa danh sách lệnh hiển thị trong menu

search_engine.py: Chứa hàm tìm kiếm YouTube.

downloader.py: Chứa logic yt-dlp để:
  - download_audio_mp3(): Tải và convert nhạc YouTube
  - download_tiktok_video(): Tải video TikTok

requirements.txt: Danh sách thư viện (python-telegram-bot, yt-dlp, python-dotenv).

.env: Lưu BOT_TOKEN và ALLOWED_TELEGRAM_IDS (nếu cần giới hạn user).

6. Các lệnh có sẵn (Available Commands)
/start - Khởi động bot và hiển thị thông báo chào mừng
/help - Hiển thị menu trợ giúp đầy đủ
/search <tên bài hát> - Tìm kiếm và tải nhạc từ YouTube (MP3)
/dowtiktok <URL> - Tải video từ TikTok

7. Giới hạn và Lưu ý (Limits & Notes)
- YouTube: Chỉ tải bài hát dưới 30 phút, output là MP3
- TikTok: Chỉ tải video dưới 10 phút, output là video gốc
- Xử lý lỗi: Video riêng tư, bị chặn, giới hạn độ tuổi
- Permission: Có thể giới hạn user thông qua ALLOWED_TELEGRAM_IDS trong .env