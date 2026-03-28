import argparse
import json
import os
import glob

parser = argparse.ArgumentParser(description='Convert word onsets to JSON format')
parser.add_argument('input', type=str, help='Path to a word onsets file or directory')
parser.add_argument('--output', type=str, default=None, help='Output JSON file path (default: same name with .json)')
parser.add_argument('--all', action='store_true', help='Convert all _word_onsets.txt files in the directory')
args = parser.parse_args()


def convert_onsets_to_json(input_path, output_path=None):
    """Convert a single word onsets file to JSON."""
    words = []
    with open(input_path, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split('\t')
            if len(parts) == 2:
                words.append({
                    'word': parts[0],
                    'start': float(parts[1]),
                })

    # Calculate end times from next word's onset
    for i in range(len(words) - 1):
        words[i]['end'] = round(words[i + 1]['start'], 3)

    # Last word gets a default duration of 0.3s
    if words:
        words[-1]['end'] = round(words[-1]['start'] + 0.3, 3)

    # Round start times
    for w in words:
        w['start'] = round(w['start'], 3)

    # Determine output path
    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = base + '.json'
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(words, f, indent=2)

    print(f"Converted {len(words)} words: {input_path} -> {output_path}")
    return words


if args.all:
    # Convert all onset files in directory
    pattern = os.path.join(args.input, '*_word_onsets.txt')
    files = glob.glob(pattern)
    if not files:
        print(f"No _word_onsets.txt files found in {args.input}")
        exit(1)
    for f in files:
        convert_onsets_to_json(f)
else:
    convert_onsets_to_json(args.input, args.output)