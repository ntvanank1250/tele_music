#!/usr/bin/env bash
set -euo pipefail

echo "Building và chạy Telegram Music Bot với Docker..."
echo ""

# Kiểm tra và tạo file .env
if [ ! -f .env ]; then
    echo "File .env chưa tồn tại. Tạo từ .env.example..."
    if [ -f .env.example ]; then
        cp .env.example .env
        echo "✓ Đã tạo file .env"
    else
        echo "BOT_TOKEN=your_telegram_bot_token_here" > .env
        echo "✓ Đã tạo file .env mới"
    fi
    echo ""
fi

# Kiểm tra xem token đã được cấu hình chưa
if grep -q "your_telegram_bot_token_here" .env 2>/dev/null; then
    echo "⚠️  BOT_TOKEN chưa được cấu hình!"
    echo ""
    echo "Vui lòng lấy token từ @BotFather trên Telegram:"
    echo "  1. Mở Telegram và tìm @BotFather"
    echo "  2. Gửi /newbot và làm theo hướng dẫn"
    echo "  3. Copy token nhận được"
    echo ""
    read -p "Nhập BOT_TOKEN của bạn: " bot_token
    
    if [ -n "$bot_token" ]; then
        sed -i "s|BOT_TOKEN=.*|BOT_TOKEN=$bot_token|g" .env
        echo "✓ Đã cập nhật BOT_TOKEN"
    else
        echo "❌ Token không được để trống!"
        exit 1
    fi
    echo ""
fi

# Kiểm tra xem FB_PAGE_ID đã được cấu hình chưa
if grep -q "your_facebook_page_id" .env 2>/dev/null; then
    echo "⚠️  FB_PAGE_ID chưa được cấu hình!"
    echo ""
    echo "Để sử dụng /upfb (upload TikTok lên Facebook):"
    echo "  1. Truy cập https://www.facebook.com/[your-page]"
    echo "  2. Lấy Page ID từ About > Page Info"
    echo ""
    read -p "Nhập FB_PAGE_ID của bạn (Enter để bỏ qua): " fb_page_id
    
    if [ -n "$fb_page_id" ]; then
        sed -i "s|FB_PAGE_ID=.*|FB_PAGE_ID=$fb_page_id|g" .env
        echo "✓ Đã cập nhật FB_PAGE_ID"
    else
        echo "⊘ Bỏ qua FB_PAGE_ID (không thể dùng /upfb)"
    fi
    echo ""
fi

# Kiểm tra xem FB_PAGE_ACCESS_TOKEN đã được cấu hình chưa
if grep -q "your_facebook_page_access_token" .env 2>/dev/null; then
    echo "⚠️  FB_PAGE_ACCESS_TOKEN chưa được cấu hình!"
    echo ""
    echo "Để lấy Page Access Token:"
    echo "  1. Truy cập https://developers.facebook.com/tools/explorer/"
    echo "  2. Chọn Page của bạn"
    echo "  3. Generate Access Token với quyền: pages_manage_posts, pages_read_engagement"
    echo "  4. Copy token"
    echo ""
    read -p "Nhập FB_PAGE_ACCESS_TOKEN của bạn (Enter để bỏ qua): " fb_access_token
    
    if [ -n "$fb_access_token" ]; then
        sed -i "s|FB_PAGE_ACCESS_TOKEN=.*|FB_PAGE_ACCESS_TOKEN=$fb_access_token|g" .env
        echo "✓ Đã cập nhật FB_PAGE_ACCESS_TOKEN"
    else
        echo "⊘ Bỏ qua FB_PAGE_ACCESS_TOKEN (không thể dùng /upfb)"
    fi
    echo ""
fi

# Build image
echo "Building Docker image..."
sudo docker compose build

# Stop container cũ nếu có
echo "Stopping old container..."
sudo docker compose down 2>/dev/null || true

# Start container mới
echo "Starting bot..."
sudo docker compose up -d

echo ""
echo "✓ Bot đã chạy thành công!"
echo ""
echo "Các lệnh hữu ích:"
echo "  sudo docker compose logs -f          # Xem logs realtime"
echo "  sudo docker compose restart          # Restart sau khi sửa code"
echo "  sudo docker compose down             # Stop bot"
echo ""
