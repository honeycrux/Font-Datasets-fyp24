# Font Datasets

This document is provided by the FYP24 group.

This repository holds the dataset preparation scripts used to prepare the datasets used for the FontDiffuser Classic Calligraphy project. These scripts are provided in the `scripts/` directory. Each dataset is given a label, e.g. FYP23.

The scripts are used to prepare raw datasets into [a file structure usable by the FontDiffuser Classic Calligraphy project](https://github.com/honeycrux/FontDiffuser-Classic-Calligraphy/blob/main/README.md#data-construction-changes).

There are also useful scripts for manual usage such listing file extensions or creating dataset summary. These scripts are in the `scripts/util` directory. See the files for their usage.

This repository also holds datasets released by us inside the `releases/` directory, where the released files are stored with **Git LFS**. Note that `git clone` by default only downloads pointers for LFS files, not the actual files. The actual files can be downloaded directly from GitHub or with specific `git lfs` commands.

Important: `LICENSE.txt` only applies to the contents of this repository, excluding the `releases/` directory. The datasets have separate Conditions of Use. Please consult each dataset's Conditions of Use before using them.

## Environment Setup

This project requires python 3.13, which is installed alongside other packages with the following:

```sh
conda env create -f environment.yml
conda activate font-datasets-fyp24
```

## Preparing Datasets

These datasets are used by the FYP24 group and are given a label in this repository.

#### FYP23 Dataset

- Label: FYP23
- Description: The final dataset prepared by the FYP23 group, usable for training models of the [New Font Generation From Classic Calligraphy project](https://github.com/lylee0/New-Font-Generation-from-Classic-Calligraphy)
- License: MIT license
- Conditions of Use: License and copyright notice (See https://choosealicense.com/licenses/mit/)

Dataset summary:

- Number of fonts: 19
- Number of characters: 56916
- Characters per font: Range 2985-3000 Mean 2995.58 SD 5.98

Download and prepare dataset:

```sh
sh scripts/fyp23/prepare-fyp23-dataset.sh
```

The content font used is PMingLiu.

The 19 target fonts used are:

| Directory | Font Name      | Word Centering      |
| --------- | -------------- | ------------------- |
| id_0      | 851tegakizatsu | Shifted Left & Up   |
| id_1      | Biaukai        | Shifted Left & Down |
| id_2      | (unknown)      | Centered            |
| id_3      | (unknown)      | Centered            |
| id_4      | (unknown)      | Centered            |
| id_5      | CSuHK          | Centered            |
| id_6      | CXingHK        | Shifted Left & Up   |
| id_7      | CSuHK          | Shifted Left & Up   |
| id_8      | Hannotate      | Shifted Left & Down |
| id_9      | Libian         | Shifted Left & Down |
| id_10     | LingWai        | Shifted Left        |
| id_11     | MCuteHK        | Shifted Left & Up   |
| id_12     | (unknown)      | Centered            |
| id_13     | Pingfong       | Shifted Left        |
| id_14     | (unknown)      | Shifted Down        |
| id_15     | PienPien       | Shifted Left & Down |
| id_16     | Xingkai        | Shifted Left & Down |
| id_17     | (unknown)      | Shifted Right       |
| id_18     | Wawati         | Shifted Left & Down |

#### LTJX Dataset

- Label: LTJX
- Description: The Lantingji Xu dataset, usable for training models of the [New Font Generation From Classic Calligraphy project](https://github.com/lylee0/New-Font-Generation-from-Classic-Calligraphy)
- Reference: https://learning.hku.hk/ccch9051/group-24/items/show/34
- License: Unknown
- Conditions of Use: Unknown

Download manually: https://github.com/honeycrux/Font-Datasets-fyp24/blob/main/releases/ltjx-dataset-source.zip

Image processing of character images is done by the FYP23 group.

The dataset structure is explained as follows:
- `for-fyp23`: The Lantingji Xu dataset in the format for Font Diff-based model and according to the use cases of the FYP23 group.
    - `lantingjixu_authentic.txt`: The authentic transcription of Lantingji Xu.
    - `strokelist.txt`: A subset of [the Diff-Font stroke list](https://github.com/HensonChen/Diff-font/blob/main/traditional_chinese_stroke.txt) consisting of stroke information of 3000 Chinese characters.
    - `wordlist.txt`: A list of 3000 words appearing in the Diff-Font stroke list used by the FYP23 project group. There are 169 unique words in Lantingji Xu that appear in this list. Subsequently, the 169 unique words are chosen to be the train set. The other 40 words are chosen to be the test set. We inherited their choice of train-test split (Minor differences: We switched to `lantingjixu_text.txt` instead of the authentic version that they use. As a result, our split by character count is actually 169-36 instead of 169-40. Additionally, they strictly use unique characters in training, but we allow images of the same characters. As a result, our split by image count is 255-50.)
    - `lacklist.txt`: A list of 40 words appearing in`lantingjixu_authentic.txt` but not in `wordlist.txt`.
    - `lacklist_strokes.txt`: Stroke information of the 40 words from `lacklist.txt` in the same order as `lacklist.txt`.
    - `full-dataset`: The whole Lantingji Xu dataset.
        - `in-word-list`: Images of words in `wordlist.txt`. Images are titled `ddddd.png` where `ddddd` is a five-digit number which indexes its corresponding character label in `wordlist.txt` starting at `00000`. If there are more than one image of a character, the title is `ddddd_i.png` where `i` is a sequence number starting from 2.
        - `not-in-word-list`: Images of words in `lacklist.txt`. The images are given an arbitrary five-digit number in the format of `_ddddd.png` (which is not an index into `lacklist.txt`). If there are more than one image of a character, the title is `_ddddd_i.png` where `i` is a sequence number starting from 2.
    - `selected-for-finetune-and-test`: The finetune and test set, subset of the `in-word-list` set, placed under the `content`/`data` subdirectories according to the training data file tree used by FYP23 models. This set consists of 169 words without repeating characters and is used for finetuning and testing by the FYP23 group.
- `for-fyp24`: The Lantingji Xu dataset in the format for FontDiffuser-based model and according to the use cases of the FYP24 group.
    - `lantingjixu_text.txt`: The transcription of Lantingji Xu with obscure characters substituted with more commonly-used Chinese characters. The FYP24 group uses this in place of the authentic version used by the FYP23 group.
    - `lantingjixu_train.txt`: A list of 169 words in the train set, which is an unordered subset of `lantingjixu_text.txt`.
    - `lantingjixu_test.txt`: A list of 36 words in the test set, which is an unordered subset of `lantingjixu_text.txt`.
    - `full-dataset`: The whole Lantingji Xu dataset, based on `lantingjixu_text.txt`, placed under the `ContentImage`/`TargetImage` subdirectories according to the training data file tree used by FYP24 models. In the training context where the whole LTJX dataset is unseen, the full dataset is used for testing by the FYP24 group.
    - `selected-for-train`: The train set, subset of the full dataset. In the training context where the LTJX dataset is used for finetuning, the train/test split is used.
    - `selected-for-test`: The test set, subset of the full dataset.

#### CASIA Dataset

- Label: CASIA
- Description: A large dataset of handwritten Chinese characters
- Reference: https://nlpr.ia.ac.cn/databases/handwriting/Home.html
- License: All rights reserved
- Conditions of Use: Research purposes only, acknowledgement required (See https://nlpr.ia.ac.cn/databases/handwriting/Application_form.html)

Dataset summary:

- Number of fonts: 337
- Number of characters: 1288010
- Characters per font: Range 19-3864 Mean 3821.99 SD 258.36

Download and prepare dataset:

```sh
sh scripts/casia/prepare-casia-dataset.sh
```

#### ZHUOJG Dataset

- Label: ZHUOJG
- Description: A Chinese calligraphy dataset consisting of 9 calligraphers in Regular Script (楷書), 6 in Running Script (行書), and 4 in Clerical Script (隶書)
- Reference: https://github.com/zhuojg/chinese-calligraphy-dataset
- License: Apache-2.0 license
- Conditions of Use: License and copyright notice, state changes (See https://choosealicense.com/licenses/apache-2.0/)

Dataset summary:

- Number of fonts: 19
- Number of characters: 138499
- Characters per font: Range 5990-9780 Mean 7289.42 SD 1078.03

Download and prepare dataset:

```sh
sh scripts/zhuojg/prepare-zhuojg-dataset.sh
```

#### NEUMASON Dataset

- Label: NEUMASON
- Description: A large Chinese font dataset
- Reference: https://github.com/neumason/Chinese-Fonts-Dataset
- License: Unknown
- Conditions of Use: Unknown

Dataset summary:

- Number of fonts: 179
- Number of characters: 1433056
- Characters per font: Range 918-9168 Mean 8005.90 SD 1305.65

Download and prepare dataset:

```sh
sh scripts/neumason/prepare-neumason-dataset.sh
```

## Other Datasets

These datasets are not used by the FYP24 group. These datasets are not given labels or scripts to prepare them into the FontDiffuser format. Though, one may use similar methodologies from the other scripts to prepare the datasets.

#### FYP23 Legacy Dataset

- Description: This dataset is prepared by the FYP23 group. The data format is the same as the FYP23 Dataset. Used by the FYP23 group for training.
- License: MIT license
- Conditions of Use: License and copyright notice (See https://choosealicense.com/licenses/mit/)

Download manually: https://github.com/honeycrux/Font-Datasets-fyp24/blob/main/releases/fyp23-legacy-dataset-source.zip

The content font used is PMingLiu.

The 19 target fonts used are: 851tegakizatsu, Baoli, Biaukai, Ching1, Ching5p, CSuHK, CXingHK, GinWuen, Hannotate, Libian, LingWai, MCuteHK, PienPien, Pingfong, SunYu, Wawati, Xingkai, Yuanti, and Yuppy.

#### Anny's Handwriting Dataset

- Description: This dataset is prepared by the FYP23 group. This dataset contains the same 169 words as the LTJX dataset's `for-fyp23/selected-for-finetune-and-test` dataset. This dataset is used by the FYP23 group for testing together with the LTJX finetune and test set.
- License: MIT license
- Conditions of Use: License and copyright notice (See https://choosealicense.com/licenses/mit/)

Download manually: https://github.com/honeycrux/Font-Datasets-fyp24/blob/main/releases/annys-handwriting-dataset-source.zip

The data is placed under the `content`/`data_*` subdirectories according to the training data file tree used by FYP23 models. Subdirectories `data_natural` and `data_messy` can be used interchangeably as the data directory. The two directories have the same set of characters, but `data_messy` is a messier version of `data_natural`.

## Running Tests

The dataset preparation scripts with important logic are tested.

The tests can be run with the following command:

```sh
pytest tests/
```

## FAQ

#### Do I need a balanced dataset?

A balanced dataset is one where each character appears in every font style. All datasets produced with the methods above do not guarantee balance.

In FontDiffuser training, a balanced dataset is only required when training when training with SCR, since counter-samples of the same character has to be chosen from other fonts (consult the training parameters to see if SCR is used). We provide `scripts/util/balance_dataset.py` to balance a dataset **by deleting in-place all characters that does not appear in all fonts**.
