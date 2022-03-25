import os
from pathlib import Path
import pandas as pd


def main():
    metadata: pd.DataFrame = load_metadata()
    print(metadata.head())
    print(metadata.describe())

    labeled_images: pd.DataFrame = add_image_names()
    print('\nimage names')
    print(labeled_images.head())
    labeled_images: pd.DataFrame = add_image_transcriptions(labeled_images, metadata)
    print('\ntranscriptions')
    print(labeled_images.head())
    print(labeled_images.describe())
    labeled_images.to_csv(save_location, encoding='utf-8', index=False)


def load_metadata() -> pd.DataFrame:
    # for some reason, read_csv truncates to 75k lines
    line_list = list()
    with open(metadata_file, mode='r', encoding='utf-8') as f:
        for line in f:
            line = line.replace('\n', '').split('\t')
            line_list.append(line)

    metadata = pd.DataFrame(line_list, columns=['id', 'error', 'gray', 'x', 'y', 'w', 'h',
                                                'transcription'])
    metadata = metadata.drop(columns=['gray', 'x', 'y', 'w', 'h'])
    # metadata: pd.DataFrame = pd.read_csv(metadata_file, delimiter='\t',
    #                                      names=['id', 'error', 'gray', 'x', 'y', 'w', 'h',
    #                                             'transcription'], encoding='utf-8')
    return metadata


def add_image_names() -> pd.DataFrame:
    labeled_images: pd.DataFrame = pd.DataFrame()
    for base, dirs, files in os.walk(word_images_folder):
        images = [Path(base, file) for file in files]
        images = [i for i in images if i.suffix == '.png' or i.suffix == '.jpg']
        images = pd.DataFrame({'image_location': images})
        labeled_images = pd.concat([labeled_images, images])
    return labeled_images


def add_image_transcriptions(labeled_images: pd.DataFrame, metadata: pd.DataFrame) -> pd.DataFrame:
    no_results = list()
    multiple_results = list()

    def match_data(location) -> pd.Series:
        id_query: str = Path(location).stem
        search_result = metadata[metadata['id'] == id_query]
        if search_result.shape[0] == 1:
            transcription = search_result['transcription'].values[0]
            error = search_result['error'].values[0]
        elif search_result.shape[0] == 0:
            no_results.append(id_query)
            transcription = error = pd.NA
        else:
            multiple_results.append(id_query)
            transcription = error = pd.NA
        return pd.Series([transcription, error], index=['transcription', 'error_value'])

    results = labeled_images['image_location'].apply(lambda l: match_data(l))
    labeled_images = pd.concat((labeled_images, results),axis=1)

    print(f'No matches: {len(no_results)}')
    print(f'Multiple matches: {len(multiple_results)}')

    return labeled_images


if __name__ == '__main__':
    metadata_file = Path('words_cleaned.tsv')
    word_images_folder = Path('resources/words/')
    save_location = Path('resources/results/word_metadata2.csv')
    if not save_location.parent.exists():
        os.makedirs(save_location.parent)
    main()
