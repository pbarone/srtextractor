# SRT Extractor and Translator

This script processes video files in a specified folder, generates SRT subtitle files using the faster-whisper tool, and translates non-English subtitles to English, creating a new `.en.forced.srt` file.

## Requirements

- Python 3.x
- `googletrans` library
- `tqdm` library
- `srt` library

You can install the required libraries using pip:
```sh
pip install googletrans==4.0.0-rc1 tqdm srt
```

## Setup

1. Download the faster-whisper standalone for Windows from [here](https://github.com/Purfview/whisper-standalone-win).
2. Extract the downloaded files into a directory named `faster-standalone`.

## Usage

1. Place your video files in a folder.
2. Run the script with the folder path as an argument:
```sh
python generateEnForced.py <path_to_video_folder>
```
   Alternatively, you can run the script without arguments and it will prompt you to enter the folder path.

## Example

```sh
python generateEnForced.py F:/Dev/videos
```

This will process all video files in the specified folder, generate SRT files if they don't exist, and create `.en.forced.srt` files with translated subtitles.

## Notes

- The script supports the following video file extensions: `.mp4`, `.avi`, `.mkv`, `.mov`, `.flv`, `.wmv`, `.mpeg`, `.webm`.
- Ensure that the faster-whisper executable and its dependencies are correctly placed in the `faster-standalone` directory.

## License

This project is licensed under the MIT License.