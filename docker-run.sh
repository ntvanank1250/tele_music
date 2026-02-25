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
