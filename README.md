# Telegram Music Bot

Muc tieu: bot Telegram tim nhac YouTube, trich xuat audio va gui file .mp3.

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

## Chay bot

```bash
python main.py
```

## Ghi chu
- Neu chua co ffmpeg: cai dat theo he dieu hanh (apt/brew/yum).
- Gioi han thoi luong video nen nho hon 10 phut de tranh tai qua lau.

## Phu thuoc
Xem [requirements.txt](requirements.txt).
