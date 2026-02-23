import argparse
import pickle
import os

try:
    import cmudict
except ImportError:
    print("cmudict not found. Install using: pip install cmudict")
    exit(1)

try:
    from g2p_en import G2p
    g2p = G2p()
    has_g2p = True
except ImportError:
    has_g2p = False

# Gets the dataset name from the argument
parser = argparse.ArgumentParser(description="Generate phoneme dictionary from word list")
parser.add_argument("--dataset-name", type=str, default='dataset1')
args = parser.parse_args()

word_list_path = f"files/{args.dataset_name}_word_list.txt"


# Checks if the word list has been created which is needed to continue
if not os.path.isfile(word_list_path):
    print(f"Word list not found: {word_list_path}")
    print(f"Run make_word_list.py first")
    exit(1)

# This loads CMU dictionary which is the list of known phonemes
cmu = cmudict.dict()

# Reads the word from the word list
with open(word_list_path, 'r') as f:
    words = [line.strip() for line in f if line.strip()]

print(f"Words to look up: {len(words)}")

word2phonemes = {}
missing = []

# Grabs all the word's phonemes from the CMU and adds words that arent recognized
# to the missiing list to look up later.
for word in words:
    lookup = word.lower()
    if lookup in cmu:
        phones = [p.rstrip("012") for p in cmu[lookup][0]]
        word2phonemes[lookup] = ' '.join(phones)
    else:
        missing.append(word)

print(f"Found: {len(word2phonemes)}/{len(words)}")

if missing:
    print(f"\nMissing words ({len(missing)}):")
    for w in missing:
        print(f"  {w}")

    # Try g2p-en first for automatic guessing
    if has_g2p:
        print("\nUsing g2p-en to guess pronunciations...")
        for word in list(missing):
            phones = g2p(word)
            phones_clean = [p.rstrip("012") for p in phones if len(p) > 1 or p in "ABCDEFGHIJKLMNOPQRSTUVWXYZ"]
            if phones_clean:
                phoneme_str = ' '.join(phones_clean)
                word2phonemes[word.lower()] = phoneme_str
                missing.remove(word)
                print(f"  {word} -> {phoneme_str}")

    # Then check for custom overrides (can correct g2p mistakes)
    custom_path = f"files/{args.dataset_name}_custom_phonemes.txt"
    if os.path.isfile(custom_path):
        print(f"\nFound custom phonemes file: {custom_path}")
        with open(custom_path, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                parts = line.split(None, 1)
                if len(parts) == 2:
                    word2phonemes[parts[0].lower()] = parts[1]
                    print(f"  Added: {parts[0].lower()} -> {parts[1]}")
                    if parts[0].lower() in [m.lower() for m in missing]:
                        missing = [m for m in missing if m.lower() != parts[0].lower()]
    
    if missing:
        print(f"\nStill missing {len(missing)} words: {missing}")
        print("These words will be skipped during alignment.")

pickle_path = f"files/{args.dataset_name}_word2phonemes.pickle"
with open(pickle_path, 'wb') as f:
    pickle.dump(word2phonemes, f)

print(f"\nSaved {len(word2phonemes)} word-phoneme pairs to {pickle_path}")
