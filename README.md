# Phoneme level lyrics aligner

This repository can be used to align lyrics transcripts with the corresponding audio signals. The audio signals may contain solo singing or singing voice mixed with other instruments.
It contains a trained deep neural network which performs alignment and singing voice separation jointly.
Details about the model, training, and data are described in the associated paper
> Schulze-Forster, K., Doire, C., Richard, G., & Badeau, R. "Phoneme Level Lyrics Alignment and Text-Informed Singing Voice Separation." IEEE/ACM Transactions on Audio, Speech and Language Processing (2021). doi: [10.1109/TASLP.2021.3091817](https://doi.org/10.1109/TASLP.2021.3091817). public version [available here](https://hal.telecom-paris.fr/hal-03255334/file/2021_Phoneme_level_lyrics_alignment_and_text-informed_singing_voice_separation.pdf).

If you use the model or code, please cite the paper:
```
@article{schulze2021phoneme,
    author={Schulze-Forster, Kilian and Doire, Clement S. J. and Richard, Gaël and Badeau, Roland},
    journal={IEEE/ACM Transactions on Audio, Speech, and Language Processing}, 
    title={Phoneme Level Lyrics Alignment and Text-Informed Singing Voice Separation}, 
    year={2021},
    volume={29},
    number={},
    pages={2382-2395},
    doi={10.1109/TASLP.2021.3091817}
    }
```

## Installation

Requires Python 3.10+ and PyTorch 2.x

1. Clone the repository:
    ```bash
    git clone https://github.com/josephhoxsey/lyrics-aligner.git
    ```
2. Install the conda environment:

    - If you want to run the model on a **CPU**:
      ```bash
      conda env create -f environment_cpu.yml
      ```
    - If you want to run the model on a **GPU**:
      ```bash
      conda env create -f environment_gpu.yml
      ```

3. Activate the conda environment:
    ```bash
    conda activate lyrics-aligner
    ```

4. (Optional) Install g2p-en for automatic phoneme guessing of unknown words:
    ```bash
    pip install g2p-en
    ```

## Quick Start

### All-in-one (recommended)

**CLI** — pass file paths directly:
```bash
python run_cli.py "path/to/song.wav" "path/to/lyrics.txt" --json
```

**GUI** — select files with a file picker:
```bash
python run_gui.py --json
```

### Optional flags

| Flag | Default | Description |
|------|---------|-------------|
| `--onsets` | `w` | `p` for phoneme, `w` for word, `pw` for both |
| `--vad-threshold` | `0` | Voice activity detection threshold (0 = off, 1-30 for songs with long instrumental sections) |
| `--json` | off | Also output results in JSON format |

## Manual Pipeline

If you prefer to run each step individually:

1. Prepare your directories with audio files and matching lyrics `.txt` files:
    ```bash
    mkdir my_audio
    mkdir my_lyrics
    ```

2. Generate a word list from your lyrics:
    ```bash
    python make_word_list.py my_lyrics --dataset-name my_dataset
    ```

3. Generate the phoneme dictionary:
    ```bash
    python make_phoneme_dict.py --dataset-name my_dataset
    ```
    This automatically looks up pronunciations using the CMU Pronouncing Dictionary. Words not found (slang, names, etc.) will be guessed using g2p-en if installed.

    To manually override any phoneme mappings, create `files/my_dataset_custom_phonemes.txt` with one entry per line:
    ```
    zombified  Z AA M B IH F AY D
    forgiato   F AO R JH EY T OW
    ```

4. Run alignment:
    ```bash
    python align.py my_audio my_lyrics --lyrics-format w --onsets w --dataset-name my_dataset --vad-threshold 0
    ```

5. (Optional) Convert results to JSON:
    ```bash
    python convert_to_json.py outputs/my_dataset/word_onsets/song_name_word_onsets.txt
    ```

## Data Preparation

### Audio
Audio is loaded using librosa, so all formats it supports can be used (.wav, .mp3, etc.). See [the documentation](https://librosa.org/doc/latest/index.html) for more details.

### Lyrics
Each lyrics file must be in `.txt` format and have the same name as the corresponding audio file (e.g. `song1.wav` → `song1.txt`).

#### Phoneme-based lyrics

If your lyrics are already decomposed into phonemes:
- Only the 39 ARPAbet phonemes listed on the [CMU Pronouncing Dictionary website](http://www.speech.cs.cmu.edu/cgi-bin/cmudict) are supported.
- The `.txt` file should contain one phoneme per line.
- The first and last symbol should be the space character: `>`. It should also be placed between words or where silence is expected.
- In this case only phoneme onsets (not word onsets) can be computed.

## Acknowledgment

This project has received funding from the European Union's Horizon 2020 research and innovation programme under the Marie Skłodowska-Curie grant agreement No. 765068.

## Copyright

Copyright 2021 Kilian Schulze-Forster of Télécom Paris, Institut Polytechnique de Paris. Licensed under the [MIT License](LICENSE).