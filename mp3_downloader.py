import argparse
from pathlib import Path

import yt_dlp


def download_mp3(url: str, output_dir: str, quality: str = "0") -> None:
    """Download the audio from a URL and convert it to MP3."""
    out_dir = Path(output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": str(out_dir / "%(title)s.%(ext)s"),
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": quality,
            }
        ],
        "quiet": False,
        "no_warnings": False,
        "noplaylist": False,
        "restrictfilenames": False,
    }

    print(f"Downloading: {url}")
    print(f"Saving to: {out_dir}")

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    print(f"Download complete. Files are in: {out_dir}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Download audio from a supported URL and convert it to MP3.")
    parser.add_argument("--url", required=True, help="The video/audio URL to download.")
    parser.add_argument("--output-dir", default="./downloads", help="Folder where MP3 files will be saved.")
    parser.add_argument(
        "--quality",
        default="0",
        help="MP3 quality. Lower is better quality (example: 0 = best, 5 = medium, 9 = worst).",
    )
    args = parser.parse_args()

    download_mp3(args.url, args.output_dir, args.quality)


if __name__ == "__main__":
    main()
