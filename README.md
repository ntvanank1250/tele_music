# Telegram Music Bot

Muc tieu: bot Telegram tim nhac YouTube, trich xuat audio, tai video TikTok, upload len Facebook Page va kiem tra thong tin he thong.

## Yeu cau
- Python 3.10+ (khuyen nghi 3.11)
- ffmpeg da duoc cai dat tren may chu
- Docker (tuy chon, de su dung tinh nang /sys kiem tra containers)
- Supervisor (tuy chon, de su dung tinh nang /sys kiem tra programs)

## Cai dat moi truong (venv)
1) Tao va cai dependencies:

```bash
./setup_venv.sh
```

2) Kich hoat venv:

```bash
source .venv/bin/activate
```

3) Tao file .env:

```bash
cp .env.example .env
```

Sau do mo file .env va dien BOT_TOKEN cua ban.
Neu muon dung /upfb, can them FB_PAGE_ID va FB_PAGE_ACCESS_TOKEN.

## Chay bot

```bash
python main.py
```

## Cac lenh co san
- /start - Khoi dong bot
- /help - Hien thi huong dan
- /search <ten bai hat> - Tim va tai nhac YouTube (MP3)
- /dowtiktok <URL> - Tai video TikTok
- /upfb <URL...> - Tai TikTok va upload len Facebook Page
- /sys - Kiem tra thong tin he thong (CPU, RAM, Disk, Docker, Supervisor)

## Ghi chu
- Neu chua co ffmpeg: cai dat theo he dieu hanh (apt/brew/yum).
- Gioi han thoi luong: YouTube < 30 phut, TikTok < 10 phut.
- /upfb chi ho tro TikTok va can Facebook Graph API token.
- /sys hien thi thong tin he thong, Docker containers va Supervisor programs.

## Phu thuoc
Xem [requirements.txt](requirements.txt).
