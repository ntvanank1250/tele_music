# Telegram Music Bot

Muc tieu: bot Telegram tim nhac YouTube, trich xuat audio, tai video TikTok va upload len Facebook Page.

## Yeu cau
- Python 3.10+ (khuyen nghi 3.11)
- ffmpeg da duoc cai dat tren may chu

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

## Ghi chu
- Neu chua co ffmpeg: cai dat theo he dieu hanh (apt/brew/yum).
- Gioi han thoi luong: YouTube < 30 phut, TikTok < 10 phut.
- /upfb chi ho tro TikTok va can Facebook Graph API token.

## Phu thuoc
Xem [requirements.txt](requirements.txt).
