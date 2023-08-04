# Overview

**Data** and **codes** for the paper "Chemical Reaction Practicality Judgment via Deep Symbol Artificial Intelligence". 

- [Overview](#overview)
- [User Guide](#user-guide)
- [Data](#data)
- [Codes](#codes)
- [License](#license)


# User Guide

## System Requirements
### Hardware requirements
Our model requires only a standard computer with enough RAM to support in-memory operations.

### Software requirements
There is no restriction on the system, like Windows or Linux, but we recommend **Ubuntu 16.04**.

The followings are runtime requirements:

1. python 2.7 or higher
2. [keras](https://github.com/keras-team/keras) 1.2.0 or higher
3. [TensorFlow](https://www.tensorflow.org/install/) 0.9.0 or higher (keras backend engines)
3. [RDKit](http://www.rdkit.org/docs/index.html)
4. [cuDNN](https://docs.nvidia.com/deeplearning/sdk/cudnn-install/) (recommended if you plan on running Keras on GPU).


### Environment setup
We strongly suggest you to use [`conda`](https://www.anaconda.com/download/) to control the virtual environment. 
```
wget -c https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
```
After installation, we create the [`conda`](https://www.anaconda.com/download/) virtual environment by the following commands:
```
conda create -n chem_env python=2.7
source activate chem_env
```


### Package installation
You can install the packages by `conda install package_name`.
```
conda install keras
conda install tensorflow
conda install tensorflow-gpu # recommended 
conda install numpy
conda install progressbar
conda install -c conda-forge rdkit
```

## Downloading the Package

Because the data are stored with [Git-LFS](https://git-lfs.github.com/), the operating system must installed with [Git-LFS](https://git-lfs.github.com/).

### Git-LFS installation

``` 
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | sudo bash
sudo apt-get install git-lfs
git lfs install 
```

### Data downloading 
```
git lfs clone https://github.com/jshmjs45/data_for_chem.git
```

Entering the *data\_for\_chem* folder, you may find two folders (data, codes) and two
files (LICENSE, README.md):


1. codes: the source code;
2. data: data for our model;
3. LICENSE: license statement;
4. README.md: the readme formatted with Markdown;



## Data Preparation
In this guide, we take the dataset `USPTO_real1` as an example. Enter the `data/data_for_practicality_judgment` folder and unzip the preprocessed file `USPTO_real1.tar.gz`:

```
cd data_for_chem
tar -xzvf data/data_for_practicality_judgment/USPTO_real1.tar.gz
```

Then activate the virtual environment and process the dataset:

```
source activate chem_env
python codes/data_process.py --folder USPTO_real1 --data data/data_for_practicality_judgment/USPTO_real1
```

## Data Formatting and Embedding Generating
We use `myio.py` to format the input data to feed to the neural network.

```
python codes/myio.py --folder USPTO_real1
```

In the output directory specified in `myio.py`, the formatted data vocabulary is produced with two folders - **train/** and **test/** which contain input sequences for training and evaluation. 

The steps above cost about 10 minutes.

##  Practicality Judgment


For Practicality Judgment, execute `class_siamese_final.py`:

```
python codes/class_siamese_final.py --data USPTO_real1 --folder USPTO_real1
```

If GPU is available, the gpu devices can be restricted:
 
```
CUDA_VISIBLE_DEVICES=0 python codes/class_siamese_final.py --folder USPTO_real1 --data USPTO_real1 
```

Then the terminal will show the training and evaluation results.

For one epoch, the model normally takes about 10 minutes with GPU device.









# Data
 
**The data is currently not available due to copyright regulations set by the collaborating company. If you require access, please feel free to email me at jshmjs45@gmail.com. (2023/08/04)**

All files are encoded in UTF-8 without Byte Order Mark (BOM).

## original\_data
This zipped file includes five files:

1. data\_from\_USPTO\_utf8
2. data\_from\_CJHIF\_utf8
3. data\_from\_ChemicalAI\_Rule\_utf8
4. data\_from\_ChemicalAI\_Real\_1\_utf8
5. data\_from\_ChemicalAI\_Real\_2\_utf8


### data\_from\_USPTO_utf8 
**Positive reactions from USPTO (USPTO)**

This public chemical reaction dataset was extracted from the US patents grants and applications dating from 1976 to September 2016 [US patents grants and applications dating from 1976 to September 2016][1] by [Daniel M. Lowe][2]. The portion of granted patents contains 1,808,938 reactions described using SMILES. Such reaction strings are composed of three groups of molecules: the reactants, the reagents, and the products, which are separated by a ‘>’ sign. After data cleaning with RDKit, an open-source cheminformatics and machine learning tool, it remained 269,132 items at
last.

The data format is 
> reactants>reagents>products PatentNumber ParagraphNum Year TextMinedYield CalculatedYield.

[1]: https://figshare.com/articles/Chemical_reactions_from_US_patents_1976-Sep2016_/5104873 "data download link"

[2]: https://www.repository.cam.ac.uk/handle/1810/244727  "D. M. Lowe, Extraction of chemical structures and reactions from the literature, Ph.D. thesis, University of Cambridge (2012)"

### data\_from\_CJHIF_utf8 
**Positive reactions from CJHIF(CJHIF)**

3,219,165 reactions mined from high impact factor journals3 with reagent, solvent and
catalyst information, in addition with yield. After data cleaning and selection, we used
the remaining 1,763,731 items at last. The reaction with expanded information is shown as follows:
> COC(=O)CCC(Cl)=O>>COC(=O)CCC=O§[CH3:6][C:7]([Cl:8])=[O:9]>>[CH3:6][CH:7]=[O:9]§COC(C)=O;§2,6-dimethylpyridine|hydroge§tetrahydrofuran§palladium on activated charcoal§55

The format of the reaction line is
>reaction§reaction with atom-mapping§functional group 1;§functional group 2;§reagent 1|reagent 2§solvent 1|solvent 2 §catalyst 1|catalyst 2§yield

where >> is the separator to separate the left part (reactant) and the right part (product). Different from USPTO, reaction conditions contain the reagents, solvents and catalysts parts.

###    data\_from\_ChemicalAI\_Rule\_utf8
**Rule-generated negative reactions from Chemical.AI (Chemical.AI-Rule)**

For every product in the positive reaction sets, we adopt a set of chemical rules to generate
all possible reactions which may output the respective products. Then we filter the
resulted reactions by a very large known positive reaction set from Chemical.AI (which
contains 20 million known reactions collected from chemical pieces of literature and patents).
Namely, all the remained unreported reactions are taken as negative reactions. Due to
memory limitation, we keep 100K rule-generated negative reactions in our dataset.
The data format is 
>reactants>>products

###    data\_from\_ChemicalAI\_Real\_1\_utf8 ( according the copyright rule, it is deleted)
**Real negative reactions from Chemical.AI (Chemical.AI-Real-1)**

12,225 real failed reactions from chemical experiment record of Chemical.AI partner
laboratories. After data deduplication and canonicalization, it remained 8,797 reactions.
The data format is 
>reactants>>products

###    data\_from\_ChemicalAI\_Real\_2\_utf8 (for final test)
**Real reactions from Chemical.AI (Chemical.AI-Real-2)**

24,514 real reactions from chemical experiment record of Chemical.AI partner laboratories,
in which there are 16,137 positive reactions and 8,377 negative reactions, where
the productivity of negative reactions is 0%. This data set is equally split into two parts:
training set and test set. The data format is 
>reactants>>products \t yield \t reagents \t SMILES \t reagents name


## data\_for\_practicality\_judgment
For practicality judgment, we let the two positive sets collocate with the two negative datasets to form four combinations.

1. [CJHIF_real1](https://github.com/jshmjs45/data_for_chem/blob/master/data_for_practicality_judgment/CJHIF_real1.tar.gz)
2. [USPTO_real1](https://github.com/jshmjs45/data_for_chem/blob/master/data_for_practicality_judgment/USPTO_real1.tar.gz)
3. [CJHIF_rule](https://github.com/jshmjs45/data_for_chem/blob/master/data_for_practicality_judgment/CJHIF_rule.tar.gz)
4. [USPTO_rule](https://github.com/jshmjs45/data_for_chem/blob/master/data_for_practicality_judgment/USPTO_rule.tar.gz)

### CJHIF_real1

| Case     | train     | dev     | test    |
| -------- | --------- | ------- | ------- |
| Positive | 1,406,259 | 156,251 | 173,624 |
| Negative | 7,178     | 798     | 874     |

### USPTO_real1

| Case     | train     | dev     | test    |
| -------- | --------- | ------- | ------- |
| Positive | 217,992   | 24,221  | 26,919  |
| Negative | 7,176     | 797     | 877     |

###  CJHIF_rule

| Case     | train     | dev     | test    |
| -------- | --------- | ------- | ------- |
| Positive | 1,428,673 | 158,741 | 89,948  |
| Negative | 158,689   | 17,632  | 10,052  |

###  USPTO_rule

| Case     | train     | dev     | test    |
| -------- | --------- | ------- | ------- |
| Positive | 217,799   | 24,200  | 90,221  |
| Negative | 24,421    |2,713    | 9,779   |

# Codes

## Data processing
1. convert_file.py 
2. clear_file.py
3. select_file.py
4. combine_files.py
5. data_process.py

### convert_file.py 
We canonicalize data without atom mappings by using this code.

The parameters are as follows:

**--mode** 0:CJHIF 1:USPTO 2:Chemical.AI

**--file** input file path

Usage: `python convert_file.py [--mode MODE] [--file FILE]`

### clear_file.py 
The converted file is cleared by using this code.

The parameters are as follows:

**--mode** 0:CJHIF 1:USPTO 2:Chemical.AI

**--file** input file path

Usage: `python clear_file.py [--mode MODE] [--file FILE]`

### slelct_file.py 
The cleared file is split into train set and test set by using this code.

The parameters are as follows:

**--per** the ratio of the test set (%)

**--file** input file path

Usage: `python slelct_file.py [--per PER] [--file FILE]`

### combine_files.py

This code is used to combine the positive data and negative data and split the combined file into the training set and test set. 

**--per** the ratio of the test set (%)

**--file1** positive file path

**--file2** negative file path

Usage: `python combine_files.py [--per PER] [--file1 FILE1] [--file2 FILE2]`

### data_process.py

This code is aim to split the train set and test set to the left part and right part, generate the 'reaction step' and segment the reaction tokens. 

**--folder** the folder of the output files

**--data** path of the dataset

Usage: `python data_process.py [--folder FOLDER] [--data data]`





## Data Formatting and Embedding Generating
### myio.py

After Unsupervised Tokenization and Reaction Step Generation, we use `myio.py` to format the input data to feed to the neural network.

In the output directory specified in `myio.py` (for example, `data/USPTO`), we obtain the formatted data vocabulary with two folders, **train/** and **test/** which contain input sequences for training and evaluation. 

The output folder structure is as follows:

```
data/USPTO/
    --vocabulary
    --train/
        --reactant
        --product
        --condition
        --step
        --label (for Practicality Judgment)
    --test/
        --reactant
        --product
        --condition
        --step
        --label (for Practicality Judgment)
```

The parameters are as follows:

**--folder** the top directory of the data to process

**--mode**  0:CHIJF 1:USPTO

**--seg**   segementation method

**--iter**  number of times to run

**--size**  dimensions in embedding

The default setting is shown as follows.
```
parser.add_argument('--mode', dest='mode', type=int, default=0, help='0:CJHIF 1:USPTO')                    
parser.add_argument('--folder', dest='folder', type=str, default="/data/CJHIF")
parser.add_argument('--seg', dest='seg', type=str, default='dlg')         
parser.add_argument('--iter', dest='iter', type=int, default=10, help='number of times to run')
parser.add_argument('--size', dest='size', type=int, default=100, help='dimensions in embedding')
```
Example: `python myio.py --folder folder_name`

## Practicality Judgment
### class\_siamese\_final.py

For Practicality Judgment, we execute `class_siamese_final.py`.

The parameters are as follows:

**--data**  the top directory of the processed data after data formatting (for example, `data/USPTO`)

**--folder** where you want to save the models and logs in each epoch

**--epochs** max epoch for training

**--dim** hidden dimensions for the Siamese Network

**--maxlen** the specified max length for input sequences (truncating or zero-padding when needed)

**--mode** 0: using all features, 1: remove steps, 2: remove reaction conditions, 3: remove steps and conditions

The default setting is shown as follows.

```
parser.add_argument('--maxlen', dest='maxlen', type=int, default=100)
parser.add_argument('--layer', dest='layer', type=str, default="biLSTM")
parser.add_argument('--rateid', dest='rateid', type=int, default=0)
parser.add_argument('--dim', dest='dim', type=int, default=64)
parser.add_argument('--epochs', dest='epochs', type=int, default=30)
parser.add_argument('--mode', dest='mode', type=int, default=0)
parser.add_argument('--folder', dest='folder', type=str, default="0802-error-rule_new")
parser.add_argument('--ratio', dest='ratio', type=int, default=5)
parser.add_argument('--sample', dest='sample', type=int, default=1)
parser.add_argument('--data', dest='data', type=str, default="0802-error-rule/")
```

Example: `python class_siamese_final.py --data data/USPTO --folder USPTO_judge`

If GPU is available, then add the script in front: ``CUDA_VISIBLE_DEVICES = the GPU id
CUDA_VISIBLE_DEVICES = 0 python class_siamese_final.py --data data/USPTO_Rule --folder USPTO_Rule``

Then the terminal will show the training and evaluation results.


# License

This project is covered under the **MIT License**.
