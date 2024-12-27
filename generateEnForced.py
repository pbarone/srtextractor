import os
import re
from googletrans import Translator
from tqdm import tqdm
import srt
import subprocess
import sys

# Define supported video file extensions and configuration for the SRT generator
VIDEO_EXTENSIONS = {".mp4", ".avi", ".mkv", ".mov", ".flv", ".wmv", ".mpeg", ".webm"}
SRT_GENERATOR_PATH = r"faster-whisper\faster-whisper-xxl.exe"
SRT_GENERATOR_ARGS = ["--multilingual", "true", "--model", "medium", "--output_dir", "source", "--beep_off", "--skip", "--print_progress", "--batch_recursive"]

def get_video_files(folder_path):
    """
    Recursively searches for video files in the specified folder and its subfolders.
    
    Args:
        folder_path (str): Path to the folder to search
        
    Returns:
        list: List of full paths to video files with supported extensions
    """
    video_files = []
    for root, _, files in os.walk(folder_path):
        for file in files:
            if os.path.splitext(file)[1].lower() in VIDEO_EXTENSIONS:
                sanitized_path = os.path.join(root, file)
                video_files.append(os.path.normpath(sanitized_path))
    return video_files

def generate_srts(video_folder):
    """
    Generates SRT subtitle files for videos using the faster-whisper tool.
    
    Args:
        video_folder (str): Path to the folder containing video files
        
    Prints success message or error if the generation fails
    """
    command = [SRT_GENERATOR_PATH, video_folder] + SRT_GENERATOR_ARGS
    try:
        subprocess.run(command, check=True)
        print("srt file generated!")
        
    except subprocess.CalledProcessError as e:
        print(f"An error occurred: {e}")

def process_srt(input_file):
    """
    Processes an SRT file by translating non-English subtitles to English.
    Creates a new .en.forced.srt file containing only the translated subtitles.
    
    Args:
        input_file (str): Path to the input SRT file
    """
    base_name, _ = os.path.splitext(input_file)
    output_file_name = f"{base_name}.en.forced.srt"
    translator = Translator()

    # Prevent path traversal attacks by sanitizing the input file path
    base_name = os.path.basename(input_file)
    safe_path = os.path.join(os.path.dirname(input_file), base_name)
    
    # Read and parse the original SRT file
    with open(safe_path, 'r', encoding='utf-8') as file:
        subtitle_generator = srt.parse(file)
        subtitles = list(subtitle_generator)

    translated_subtitles = []

    # Process each subtitle, translating non-English text
    for subtitle in tqdm(subtitles, desc="Processing Subtitles", unit="subtitle"):
        detected_lang = translator.detect(subtitle.content).lang
        if detected_lang != 'en':
            translated_text = translator.translate(subtitle.content, src='auto', dest='en').text
            if subtitle.content != translated_text:
                new_subtitle = srt.Subtitle(
                    index=subtitle.index,
                    start=subtitle.start,
                    end=subtitle.end,
                    content=translated_text
                )
                translated_subtitles.append(new_subtitle)

    # Write the translated subtitles to a new file
    with open(output_file_name, "w", encoding="utf-8") as output_file:
        output_file.write(srt.compose(translated_subtitles))

def main():
    """
    Main function that orchestrates the subtitle generation and translation process.
    Accepts folder path as command line argument or prompts user for input.
    """
    # Get the base folder path from command line or user input
    if len(sys.argv) > 1:
        base_folder = sys.argv[1]
    else:
        base_folder = input("Please enter the folder path containing video files: ")

    # Validate the folder path
    while not os.path.exists(base_folder) or not os.path.isdir(base_folder):
        base_folder = input("Invalid folder path. Please enter a valid folder path: ")

    print(f"Processing folder: {base_folder}")

    # Generate SRT files for videos that don't have them
    generate_srts(base_folder)

    # Process all video files in the folder
    video_files = get_video_files(base_folder)

    # Iterate through videos and process their SRT files
    for video_file in video_files:
        file_name_with_ext = os.path.basename(video_file)
        file_name = os.path.splitext(file_name_with_ext)[0]
        srt_file = os.path.splitext(video_file)[0] + ".srt"
        srt_forced = os.path.splitext(video_file)[0] + ".en.forced.srt"

        # Skip if SRT file doesn't exist or forced SRT already exists
        if not os.path.exists(srt_file):
            print(f"- {file_name} - .srt file not found")
            continue

        if os.path.exists(srt_forced):
            print(f"- {file_name} - Found .en.forced.srt file")
            continue
        else:
            print(f"- {file_name} - Found .srt file")
            process_srt(srt_file)

if __name__ == "__main__":
    main()
