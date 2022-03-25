# This cleans the IAM database `words.txt` file in data/ascii.tgz, as downloaded from:
# https://fki.tic.heia-fr.ch/databases/download-the-iam-handwriting-database

from pathlib import Path


def clean_words():
    file = Path('../words.txt')
    new_file = Path('../words_cleaned.tsv')
    with open(file, mode='r', encoding='ascii') as f:
        with open(new_file, mode='w', encoding='utf-8') as s:
            for line in f:
                cols = line.count(' ') + 1
                if line[0] != '#' and cols >= 9:
                    cleaned_line = line.split(' ', 8)
                    cleaned_line.pop(7)  # drop the buggy grammatical tag column
                    cleaned_line = '\t'.join(cleaned_line)  # change back to string, tab-separated
                    s.write(cleaned_line)


if __name__ == '__main__':
    clean_words()
