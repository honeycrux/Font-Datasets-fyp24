# Font Datasets

This document is provided by the FYP24 group.

This repository holds the dataset preparation scripts used to prepare the datasets used for the FontDiffuser Classic Calligraphy project. Each dataset is given a label, e.g. FYP23.

Provided are raw datasets and scripts that prepare them into [a file structure usable by the FontDiffuser Classic Calligraphy project](https://github.com/honeycrux/FontDiffuser-Classic-Calligraphy/blob/main/README.md#data-construction-changes).

Important: The datasets have separate Conditions of Use from the one used in this repository. Please be mindful of each dataset's Conditions of Use before using them.

## Environment Setup

This project requires python 3.13, which is installed alongside other packages with the following:

```sh
conda env create -f environment.yml
conda activate font-datasets-fyp24
```

## Preparing Datasets

#### FYP23 Legacy Dataset

This dataset is deprecated. The data format is the same as the FYP23 Dataset.

The content font used is PMingLiu.

The 19 target fonts used are: 851tegakizatsu, Baoli, Biaukai, Ching1, Ching5p, CSuHK, CXingHK, GinWuen, Hannotate, Libian, LingWai, MCuteHK, PienPien, Pingfong, SunYu, Wawati, Xingkai, Yuanti, and Yuppy.

#### FYP23 Dataset

- Label: FYP23
- Description: The final dataset prepared by the FYP23 group, usable for training models of the [New Font Generation From Classic Calligraphy project](https://github.com/lylee0/New-Font-Generation-from-Classic-Calligraphy)
- License: MIT license
- Conditions of Use: License and copyright notice (See https://choosealicense.com/licenses/mit/)

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

#### CASIA Dataset

- Label: CASIA
- Description: A large dataset of handwritten Chinese characters
- Reference: https://nlpr.ia.ac.cn/databases/handwriting/Home.html
- License: All rights reserved
- Conditions of Use: Research purposes only, acknowledgement required (See https://nlpr.ia.ac.cn/databases/handwriting/Application_form.html)

```sh
sh scripts/prepare-casia-dataset.sh
```

#### ZHUOJG Dataset

- Label: ZHUOJG
- Description: A Chinese calligraphy dataset consisting of 9 calligraphers in Regular Script (楷書), 6 in Running Script (行書), and 4 in Clerical Script (隶書)
- Reference: https://github.com/zhuojg/chinese-calligraphy-dataset
- License: Apache-2.0 license
- Conditions of Use: License and copyright notice, state changes (See https://choosealicense.com/licenses/apache-2.0/)

```sh
sh scripts/prepare-zhuojg-dataset.sh
```

#### NEUMASON Dataset

- Label: NEUMASON
- Description: A large Chinese font dataset
- Reference: https://github.com/neumason/Chinese-Fonts-Dataset
- License: Unknown
- Conditions of Use: Unknown

```sh
sh scripts/neumason/prepare-neumason-dataset.sh
```

## FAQ

#### Do I need a balanced dataset?

A balanced dataset is one where each character appears in every font style. All datasets produced with the methods above do not guarantee balance.

In FontDiffuser training, a balanced dataset is only required when training when training with SCR, since counter-samples of the same character has to be chosen from other fonts (consult the training parameters to see if SCR is used). We provide `scripts/util/balance_dataset.py` to balance a dataset **by deleting in-place all characters that does not appear in all fonts**.
