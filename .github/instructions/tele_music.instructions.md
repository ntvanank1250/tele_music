Project Instructions: Python Telegram Music Bot
1. Mục tiêu (Core Objective)
Xây dựng Telegram Bot bằng Python cho phép người dùng tìm kiếm nhạc từ YouTube, trích xuất âm thanh và gửi file .mp3 trực tiếp.

2. Công nghệ yêu cầu (Tech Stack)
Framework: python-telegram-bot (version 20.x trở lên, sử dụng asyncio).

Tìm kiếm: Youtube-python hoặc yt-search.

Xử lý Audio: yt-dlp (Công cụ mạnh mẽ và cập nhật nhất hiện nay).

Yêu cầu hệ thống: Máy chủ cần cài đặt sẵn ffmpeg để convert audio.

3. Cấu trúc Logic (Flow Logic)
Lệnh /search [tên bài hát]:

Bot gọi VideosSearch để lấy 5 kết quả hàng đầu.

Trả về tin nhắn kèm InlineKeyboardMarkup. Mỗi nút chứa callback_data là ID của video.

Xử lý Callback (Khi bấm nút):

Hiển thị thông báo "Đang xử lý âm thanh... 🎧".

Sử dụng yt-dlp với option postprocessors để trích xuất audio định dạng .mp3.

Sử dụng context.bot.send_audio để gửi file.

Tối ưu hóa bộ nhớ:

Xóa file tạm sau khi gửi thành công để tránh đầy ổ cứng.

Giới hạn thời lượng video (ví dụ: chỉ tải các bài < 10 phút).

4. Quy tắc lập trình (Coding Rules)
Asynchronous: Phải sử dụng async/await để bot không bị treo khi có nhiều người dùng cùng lúc.

Error Handling: Bắt lỗi DownloadError từ yt-dlp (thường do video bị chặn hoặc giới hạn độ tuổi).

Logging: Sử dụng module logging của Python để theo dõi tiến trình.

Environment: Lưu BOT_TOKEN trong file .env và dùng python-dotenv để đọc.

5. Cấu trúc File đề xuất
main.py: Khởi tạo Application và đăng ký Handlers.

search_engine.py: Chứa hàm tìm kiếm YouTube.

downloader.py: Chứa logic yt-dlp để tải và convert nhạc.

requirements.txt: Danh sách thư viện (python-telegram-bot, yt-dlp, python-dotenv).