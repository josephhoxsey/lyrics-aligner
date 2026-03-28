'''
pipeline.py
'''

import os
import shutil
import subprocess
import sys

def print_separator(count):
    print(f"\n{'='*count}")

def run_step(description, command):
    print_separator(50)
    print(f"\t{description}")
    print_separator(50)
    results= subprocess.run([sys.executable] + command)
    if results.returncode != 0:
        print(f"\nFailed: {description}")
        exit(1)

def run_pipeline(audio_path, lyric_path, onsets='w', vad_threshold=0, json_output=False):
    
    # Parse out audio info
    audio_path_map = os.path.splitext(os.path.basename(audio_path))
    song_name = audio_path_map[0]
    audio_extension = audio_path_map[1]
    dataset_name = song_name + '_dataset'

    temp_audio = 'temp_audio'
    temp_lyrics = 'temp_lyrics'

    # Create temp directories to store copies of the audio and lyrics files
    os.makedirs(temp_audio, exist_ok=True)
    os.makedirs(temp_lyrics, exist_ok=True)

    try:
        # Copies the audio and lyrics files
        shutil.copy2(audio_path, os.path.join(temp_audio, song_name + audio_extension))
        shutil.copy2(lyric_path, os.path.join(temp_lyrics, song_name + '.txt'))
        
        # Generates the word list
        run_step("Generating word list",
                ["make_word_list.py", temp_lyrics, "--dataset-name", dataset_name])
        
        # Generates the phonemes dictionary
        run_step("Generating phoneme dictionary",
                ["make_phoneme_dict.py", "--dataset-name", dataset_name])
        
        # Run Alignment
        run_step("Running alignment",
                ["align.py", temp_audio, temp_lyrics,
                "--lyrics-format", "w",
                "--onsets", onsets,
                "--dataset-name", dataset_name,
                "--vad-threshold", str(vad_threshold)])
        
        # if JSON is enabled, convert to JSON file
        if json_output:
            onset_file = os.path.join('outputs', dataset_name, 'word_onsets', song_name +'.txt')
            if os.path.isfile(onset_file):
                run_step("Converting to JSON", ["convert_to_json.py", onset_file])
            else:
                print(f"Onset file not found: {onset_file}")
    finally:
        # Clean up the temp stuff
        shutil.rmtree(temp_audio)
        shutil.rmtree(temp_lyrics)
    
    print_separator(50)
    print(f"\tDone! Check the outputs/ directory for results.")
    print_separator(50)

