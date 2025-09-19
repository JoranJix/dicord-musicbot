# 🎵 Discord Music Bot

A lightweight, self-hosted Discord music bot written in Python. Plays `.mp3` files from a local directory, supports shuffle, playback controls, and displays the current track using rich embeds.

---

## 🚀 Features

- ✅ Joins and leaves voice channels
- ▶️ Plays specific or random `.mp3` files
- 🔀 Shuffles playlist
- ⏸️ Pauses / ▶️ Resumes / ⏹️ Stops playback
- ⏭️ Skips to next track
- 📃 Lists available tracks
- 📦 Uses `.env` for secure token management
- 🎨 Displays current track as an embed

---

## 📦 Requirements

- Python 3.8+
- FFmpeg installed and available in system path
- The following Python libraries:

```sh
pip install discord.py python-dotenv PyNaCl
```
Optional (for future YouTube support):
```sh
pip install yt-dlp
```
##🛠️ Setup
1. 	Clone the repository:
```sh
git clone https://github.com/JoranJix/dicord-musicbot.git
cd musicbot
```
2. 	Create a  file
```ssh
touch .env
nano .env
```
then paste
```sh
DISCORD_TOKEN=your_discord_bot_token_here
```
3. 	Create a  folder music/ and add your mp3 files
4.  Run the bot:
```sh
 python3 bot.py
```
##⚙️ Systemd Integration (Linux
To run the bot as a service:
```sh
# /etc/systemd/system/musicbot.service
[Unit]
Description=Discord Music Bot
After=network.target

[Service]
WorkingDirectory=/path/to/your/bot
ExecStart=/usr/bin/python3 /path/to/your/bot/bot.py
Restart=on-failure
RestartSec=5
Environment="PYTHONUNBUFFERED=1"

[Install]
WantedBy=multi-user.target
```
Enable and start:
```sh
sudo systemctl daemon-reload
sudo systemctl enable musicbot
sudo systemctl start musicbot
```



##📜 License
MIT License — free to use, modify, and share
