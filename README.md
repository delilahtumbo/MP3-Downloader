# MP3 Downloader

<div align="center">
  <img src="https://raw.githubusercontent.com/delilahtumbo/MP3-Downloader/main/assets/banner.png" alt="MP3 Downloader Logo" width="650" onerror="this.style.display='none'" />

  <h3>Modern MP3 downloader with a clean desktop experience</h3>

  [![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
  [![PySide6](https://img.shields.io/badge/UI-PySide6-41CD52?style=for-the-badge&logo=qt&logoColor=white)](https://pypi.org/project/PySide6/)
  [![yt-dlp](https://img.shields.io/badge/Downloader-yt--dlp-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://github.com/yt-dlp/yt-dlp)
  [![FFmpeg](https://img.shields.io/badge/External-FFmpeg-007808?style=for-the-badge&logo=ffmpeg&logoColor=white)](https://ffmpeg.org/)
</div>

## 🎯 Overview

MP3 Downloader is a desktop application designed for downloading audio from supported online sources in a clean, streamlined, and user-friendly way. It is inspired by the polished experience of YoutubeGO, while using a Papua New Guinea-inspired visual palette: red, gold, black, and white.

This project focuses on simplicity and speed — download audio, queue multiple jobs, choose format/quality, and save files to your preferred folder without unnecessary complexity.

## 📋 Table of Contents
- [Features](#-key-features)
- [Papua New Guinea Color Palette](#-papua-new-guinea-color-palette)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Run the App](#-run)
- [Usage Tips](#-usage-tips)
- [Related Project](#-related-project)

## 🌟 Key Features

### Core Features
- Download MP3 audio from supported URLs
- Add multiple downloads to a queue
- Select a default audio format and quality
- Choose a custom download folder
- Toggle between dark and light themes
- Desktop UI built with PySide6

### User Experience
- Clean, modern interface inspired by YoutubeGO
- Easy-to-use workflow for downloading and organizing audio files
- Lightweight configuration with minimal setup
- Designed for a smooth local desktop experience

## 🎨 Papua New Guinea Color Palette

The app uses a scheme inspired by the Papua New Guinea flag:

- Red: `#CE1126`
- Gold: `#FCD116`
- Black: `#000000`
- White: `#FFFFFF`

## ⚙️ Requirements

Before you begin, make sure the following are installed:

- Python 3.10+
- FFmpeg installed and available on your `PATH`
- PySide6
- yt-dlp

## 🚀 Installation

```bash
git clone https://github.com/delilahtumbo/MP3-Downloader.git
cd MP3-Downloader
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## ▶️ Run

```bash
python main.py
```

## 🛠️ Usage Tips

- Paste a supported URL into the app and begin the download
- Use the queue to manage multiple downloads efficiently
- Choose the output folder you want to save to
- Set your preferred default audio format and quality
- Switch themes anytime from the application settings

## 🤝 Related Project

- [Efeckc17/YoutubeGO](https://github.com/Efeckc17/YoutubeGO)

This project was inspired by the clean and modern user experience of YoutubeGO, while adapting it toward a focused MP3-only download workflow.

---

<div align="center">
  <sub>Built with ❤️ for simple, fast MP3 downloads.</sub>
</div>
