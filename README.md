# MP3 Downloader

<div align="center">
  <img src="https://raw.githubusercontent.com/delilahtumbo/MP3-Downloader/main/assets/banner.png" alt="MP3 Downloader Banner" width="650" onerror="this.style.display='none'" />

  <h3>Modern MP3 downloader with a clean desktop experience</h3>

  [![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
  [![PySide6](https://img.shields.io/badge/UI-PySide6-41CD52?style=for-the-badge&logo=qt&logoColor=white)](https://pypi.org/project/PySide6/)
  [![yt-dlp](https://img.shields.io/badge/Downloader-yt--dlp-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://github.com/yt-dlp/yt-dlp)
  [![FFmpeg](https://img.shields.io/badge/External-FFmpeg-007808?style=for-the-badge&logo=ffmpeg&logoColor=white)](https://ffmpeg.org/)
</div>

## 🎯 Overview

MP3 Downloader is a lightweight desktop app for downloading MP3 audio from supported sources with a clean, beginner-friendly workflow. It blends a modern interface with a Papua New Guinea-inspired palette — red, gold, black, and white — to create a crisp, premium look.

This project is inspired by the polished user experience of YoutubeGO, but focused specifically on MP3 downloads, queue management, and easy media collection.

## 📋 Table of Contents
- [Key Features](#-key-features)
- [Papua New Guinea Color Palette](#-papua-new-guinea-color-palette)
- [Requirements](#-requirements)
- [Installation](#-installation)
- [Run the App](#-run)
- [Usage Tips](#-usage-tips)
- [Related Project](#-related-project)

## 🌟 Key Features

### 🛠️ Core Features
- Download MP3 audio from supported URLs
- Queue multiple downloads and manage them in sequence
- Select a default audio format and quality
- Choose a custom destination folder for saved files
- Toggle between dark and light themes
- Desktop UI built with PySide6

### ✨ User Experience
- Clean, modern interface inspired by YoutubeGO
- Straightforward workflow for downloading and organizing audio
- Simple settings for format, quality, and save location
- Comfortable desktop experience with a polished visual style

## 🎨 Papua New Guinea Color Palette

The app uses a palette inspired by the Papua New Guinea flag:

- Red: `#CE1126`
- Gold: `#FCD116`
- Black: `#000000`
- White: `#FFFFFF`

## ⚙️ Requirements

Make sure the following are installed before running the app:

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

## 🧭 Usage Tips

- Paste a supported URL into the app
- Add multiple files to the queue for batch downloading
- Set your preferred output folder before downloading
- Choose the default format and quality that fit your needs
- Switch themes anytime from the UI

## 🤝 Related Project

- [Efeckc17/YoutubeGO](https://github.com/Efeckc17/YoutubeGO)

This project was inspired by the clean, modern user experience of YoutubeGO while adapting it to a more focused MP3-only downloader.

---

<div align="center">
  <sub>Built with ❤️ for simple, fast, and elegant MP3 downloads.</sub>
</div>
