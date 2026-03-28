'''
run_gui.py
'''

import argparse
import tkinter as tk
from tkinter import filedialog
from pipeline import run_pipeline

root = tk.Tk()
root.withdraw()

def main():
    # Arguments
    parser = argparse.ArgumentParser(description='Run full lyric alignment pipeline')
    parser.add_argument('--vad-threshold', type=float, default=0)
    parser.add_argument('--onsets', type=str, default='w', help='p for phoneme, w for word, pw for both')
    parser.add_argument('--json', action='store_true', help='Also output JSON format')

    args = parser.parse_args()

    audio_path = filedialog.askopenfilename(
        title="Select Audio File",
        filetypes=(
            ("MP3 files", "*.mp3"),
            ("WAV files", "*.wav")
        )
    )
    if not audio_path:
        print("No audio file selected.")
        exit(1)


    lyric_path = filedialog.askopenfilename(
        title="Select Lyric File",
        filetypes=(
            ("Text files", "*.txt"),
        )
    )
    if not lyric_path:
        print("No lyrics file selected.")
        exit(1)

    run_pipeline(audio_path, lyric_path, args.onsets, args.vad_threshold, args.json)

if __name__ == '__main__':
    main()