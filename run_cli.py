'''
run_cli.py
'''

import argparse
import os
from pipeline import run_pipeline


def main():
    # Arguments
    parser = argparse.ArgumentParser(description='Run full lyric alignment pipeline')
    parser.add_argument('audio', type=str, help='Path to an audio file (wav, mp3, etc.)')
    parser.add_argument('lyrics', type=str, help='Path to a the lyrics .txt file')
    parser.add_argument('--vad-threshold', type=float, default=0)
    parser.add_argument('--onsets', type=str, default='w', help='p for phoneme, w for word, pw for both')
    parser.add_argument('--json', action='store_true', help='Also output JSON format')

    args = parser.parse_args()

    # Validate inputs
    if not os.path.isfile(args.audio):
        print(f"Audio file not found: {args.audio}")
        exit(1)
    
    if not os.path.isfile(args.lyrics):
        print(f"Lyrics file not found: {args.lyrics}")
        exit(1)

    run_pipeline(args.audio, args.lyrics, args.onsets, args.vad_threshold, args.json)

if __name__ == '__main__':
    main()

