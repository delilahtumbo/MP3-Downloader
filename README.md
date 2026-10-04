# MP3 Downloader

A lightweight Python project for downloading MP3 audio from supported video/audio sources using `yt-dlp`.

## Features
- Download MP3 audio from YouTube and other supported sites via `yt-dlp`
- Save audio files into a selected folder
- Extract high-quality MP3 output using FFmpeg
- Simple command-line interface

## Requirements
- Python 3.10+
- FFmpeg installed and available in your PATH

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

If FFmpeg is not installed:

- macOS: `brew install ffmpeg`
- Ubuntu/Debian: `sudo apt install ffmpeg`
- Windows: install FFmpeg and add it to your PATH

## Usage

Download a single video/audio URL as MP3:

```bash
python mp3_downloader.py --url "https://www.youtube.com/watch?v=VIDEO_ID"
```

Download to a custom folder:

```bash
python mp3_downloader.py --url "https://www.youtube.com/watch?v=VIDEO_ID" --output-dir ./downloads
```

Download a playlist:

```bash
python mp3_downloader.py --url "https://www.youtube.com/playlist?list=PLAYLIST_ID" --output-dir ./downloads
```

Use a lower-quality MP3 encoding:

```bash
python mp3_downloader.py --url "https://www.youtube.com/watch?v=VIDEO_ID" --quality 5
```

## Example

```bash
python mp3_downloader.py --url "https://youtu.be/dQw4w9WgXcQ" --output-dir ./downloads
```

This project is a good starter foundation and can be expanded with a graphical UI, URL validation, playlist queueing, and download history.
