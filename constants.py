"""Constants and configuration for the Telegram bot."""

# Duration limits (in seconds)
MAX_YOUTUBE_DURATION = 30 * 60  # 30 minutes
MAX_TIKTOK_DURATION = 10 * 60   # 10 minutes

# Messages
MSG_WELCOME = (
    "Chào bạn! Dùng lệnh /search <tên bài hát> để tìm nhạc.\n"
    "Dùng lệnh /help để xem hướng dẫn chi tiết."
)

MSG_HELP = """
📖 *HƯỚNG DẪN SỬ DỤNG BOT NHẠC & VIDEO*

🎵 *Các lệnh có sẵn:*

/start - Khởi động bot
/help - Hiển thị menu trợ giúp này
/search <tên bài hát> - Tìm kiếm và tải nhạc từ YouTube
/dowtiktok <URL> - Tải video từ TikTok
/upfb <URL...> - Tải TikTok và up lên Facebook
/sys - Kiểm tra thông tin hệ thống, Docker & Supervisor

📝 *Cách sử dụng:*

*🎧 Tải nhạc YouTube:*
1️⃣ Gõ lệnh /search kèm tên bài hát
   • Ví dụ: `/search Imagine Dragons Believer`
2️⃣ Bot sẽ trả về 5 kết quả phù hợp nhất
3️⃣ Chọn bài hát bạn muốn tải
4️⃣ Chờ bot xử lý và gửi file MP3 cho bạn

*🎬 Tải video TikTok:*
1️⃣ Copy link video TikTok (link đầy đủ hoặc rút gọn)
2️⃣ Gõ lệnh /dowtiktok kèm link
   • Ví dụ: `/dowtiktok https://www.tiktok.com/@user/video/123456`
   • Hoặc: `/dowtiktok https://vm.tiktok.com/xyz123`
3️⃣ Chờ bot tải và gửi video cho bạn

*📤 Up Facebook (Page):*
1️⃣ Chuẩn bị Access Token và Page ID
2️⃣ Gõ lệnh /upfb kèm 1 hoặc nhiều link TikTok
    • Ví dụ: `/upfb https://www.tiktok.com/@user/video/123456`
    • Nhiều link: `/upfb url1 url2 url3`
3️⃣ Bot sẽ tải video và upload lên Facebook Page

⚠️ *Giới hạn:*
• Nhạc YouTube: < 30 phút → MP3
• Video TikTok: < 10 phút → Video gốc
• Video riêng tư, bị chặn, hoặc giới hạn độ tuổi không tải được
• /upfb chỉ hỗ trợ TikTok và yêu cầu cấu hình FB_PAGE_ID, FB_PAGE_ACCESS_TOKEN

💡 *Mẹo:* 
• Gõ tên bài hát cụ thể kèm tên ca sĩ để kết quả chính xác hơn
• Với TikTok, cả link đầy đủ và link rút gọn đều được hỗ trợ
"""

# Command usage messages
MSG_SEARCH_USAGE = "Hãy nhập từ khóa. Ví dụ: /search Imagine Dragons"
MSG_TIKTOK_USAGE = (
    "Hãy nhập URL video TikTok.\n"
    "Ví dụ: /dowtiktok https://www.tiktok.com/@user/video/123456"
)
MSG_UPFB_USAGE = (
    "Hãy nhập URL TikTok cần upload.\n"
    "Ví dụ: /upfb https://www.tiktok.com/@user/video/123456"
)

# Error messages
MSG_UNAUTHORIZED = "Bạn không có quyền sử dụng bot."
MSG_INVALID_TIKTOK_URL = "URL không hợp lệ. Vui lòng nhập link TikTok."
MSG_NO_VALID_TIKTOK_URL = "Không tìm thấy URL TikTok hợp lệ."
MSG_VIDEO_TOO_LONG_YOUTUBE = "Video quá dài. Vui lòng chọn bài dưới 30 phút."
MSG_VIDEO_TOO_LONG_TIKTOK = "Video quá dài. Vui lòng chọn video dưới 10 phút."
MSG_DOWNLOAD_FAILED = "Không tải được. Video có thể bị chặn hoặc riêng tư."
MSG_DOWNLOAD_AUDIO_FAILED = "Không tải được âm thanh. Video có thể bị chặn hoặc giới hạn tuổi."
MSG_UNEXPECTED_ERROR = "Đã xảy ra lỗi khi xử lý yêu cầu."
MSG_FB_CONFIG_MISSING = (
    "Vui lòng thêm FB_PAGE_ID và FB_PAGE_ACCESS_TOKEN trong .env, sau đó restart bot."
)
MSG_NO_SEARCH_RESULTS = "Không tìm thấy kết quả phù hợp."
MSG_SYSTEM_INFO_ERROR = "Đã xảy ra lỗi khi thu thập thông tin hệ thống."

# Processing messages
MSG_PROCESSING_AUDIO = "Đang xử lý âm thanh... 🎧"
MSG_DOWNLOADING_TIKTOK = "Đang tải video TikTok... 🎬"
MSG_COLLECTING_SYSTEM_INFO = "Đang thu thập thông tin hệ thống... ⏳"
MSG_SELECT_SONG = "Chọn bài hát:"

# Success messages template
MSG_UPFB_PROCESSING = "Đang xử lý {}/{} video..."
MSG_UPFB_COMPLETE = "Hoàn tất.\n"
MSG_UPFB_SUCCESS = "Thành công: {}"
MSG_UPFB_FAILED_LONG = "Thất bại: video quá dài (dưới 10 phút)"
MSG_UPFB_FAILED_DOWNLOAD = "Thất bại: không tải được video TikTok"
MSG_UPFB_FAILED_UPLOAD = "Thất bại: lỗi upload Facebook"
MSG_UPFB_INVALID_LINKS = "Link không hợp lệ: {}"

# Bot commands for menu
BOT_COMMANDS = [
    ("start", "Khởi động bot"),
    ("help", "Hiển thị hướng dẫn"),
    ("search", "Tìm kiếm nhạc YouTube"),
    ("dowtiktok", "Tải video TikTok"),
    ("upfb", "Upload TikTok lên Facebook"),
    ("sys", "Thông tin hệ thống"),
]
