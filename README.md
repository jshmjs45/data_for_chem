# 1 data\_for\_science
Data for our paper "Chemical Reaction Practicality Judgment via Deep Symbol Artificial Intelligence".

 1. [original_data](https://github.com/jshmjs45/data_for_science/tree/master/original_data)
 2. [data\_for\_practicality\_judgment](https://github.com/jshmjs45/data_for_science/tree/master/data_for_practicality_judgment)

All files are encoded in UTF-8 without Byte Order Mark (BOM).

## 1.1 original\_data
This zipped file includes three files:

1. [data\_from\_USPTO\_utf8](https://github.com/jshmjs45/data_for_science/blob/master/original_data/data_from_USPTO_utf8.tar.gz)
2. [data\_from\_CJHIF\_utf8](https://github.com/jshmjs45/data_for_science/blob/master/original_data/data_from_CJHIF_utf8.tar.gz)
3. [data\_from\_ChemicalAI\_Rule\_utf8](https://github.com/jshmjs45/data_for_science/blob/master/original_data/data_from_ChemicalAI_Rule_utf8.tar.gz)
4. [data\_from\_ChemicalAI\_Real\_1\_utf8](https://github.com/jshmjs45/data_for_science/blob/master/original_data/data_from_ChemicalAI_Real_1_utf8.tar.gz)
5. [data\_from\_ChemicalAI\_Real\_2\_utf8](https://github.com/jshmjs45/data_for_science/blob/master/original_data/data_from_ChemicalAI_Real_2_utf8.tar.gz)


### 1.1.1 data\_from\_USPTO_utf8 
**Positive reactions from USPTO (USPTO)**

This public chemical reaction dataset was extracted from the US patents grants and applications dating from 1976 to September 2016 [US patents grants and applications dating from 1976 to September 2016][1] by [Daniel M. Lowe][2]. The portion of granted patents contains 1,808,938 reactions described using SMILES. Such reaction strings are composed of three groups of molecules: the reactants, the reagents, and the products, which are separated by a ‘>’ sign. After data cleaning with RDKit,an open-source cheminformatics and machine learning tool, it remained 269,132 items at
last.

The data format is 
> reactants>reagents>products PatentNumber ParagraphNum Year TextMinedYield CalculatedYield.

[1]: https://figshare.com/articles/Chemical_reactions_from_US_patents_1976-Sep2016_/5104873 "data download link"

[2]: https://www.repository.cam.ac.uk/handle/1810/244727  "D. M. Lowe, Extraction of chemical structures and reactions from the literature, Ph.D. thesis, University of Cambridge (2012)"

### 1.1.2 data\_from\_CJHIF_utf8 
**Positive reactions from CJHIF(CJHIF)**

3,219,165 reactions mined from high impact factor journals3 with reagent, solvent and
catalyst information, in addition with yield. After data cleaning and selection, we used
remaining 1,763,731 items at last. The reaction with expanded information is shown as follows:
> COC(=O)CCC(Cl)=O>>COC(=O)CCC=O§[CH3:6][C:7]([Cl:8])=[O:9]>>[CH3:6][CH:7]=[O:9]§COC(C)=O;§2,6-dimethylpyridine|hydroge§tetrahydrofuran§palladium on activated charcoal§55

The format of reaction line is
>reaction§reaction with atom-mapping§functional group 1;§functional group 2;§reagent 1|reagent 2§solvent 1|solvent 2 §catalyst 1|catalyst 2§yield

where >> is the separator to separate the left part (reactant) and the right part (product). Different from USPTO, reaction conditions contain the reagents, solvents and catalysts parts.

###	1.1.3. data\_from\_ChemicalAI\_Rule\_utf8
**Rule-generated negative reactions from Chemical.AI (Chemical.AI-Rule)**

For every product in the positive reaction sets, we adopt a set of chemical rules to generate
all possible reactions which may output the respective products. Then we filter the
resulted reactions by a very large known positive reaction set from Chemical.AI (which
contains 20 million known reactions collected from chemical literatures and patents).
Namely, all the remained unreported reactions are taken as negative reactions. Due to
memory limitation, we keep 100K rule-generated negative reactions in our dataset.
The data format is 
>reactants>>products

###	1.1.4. data\_from\_ChemicalAI\_Real\_1\_utf8
**Real negative reactions from Chemical.AI (Chemical.AI-Real-1)**

12,225 real failed reactions from chemical experiment record of Chemical.AI partner
laboratories. After data deduplication and canonicalization, it remained 8,797 reactions.
The data format is 
>reactants>>products

###	1.1.5. data\_from\_ChemicalAI\_Real\_2\_utf8 
24,514 real reactions from chemical experiment record of Chemical.AI partner laboratories,
in which there are 16,137 positive reactions and 8,377 negative reactions, where
the productivity of negative reactions is 0%. This data set is equally split into two parts:
training set and test set. The data format is 
>reactants>>products \t yield \t reagents \t SMILES \t reagents name


## 1.2 data\_for\_practicality\_judgment
1. [CJHIF_real1](https://github.com/jshmjs45/data_for_science/blob/master/data_for_practicality_judgment/CJHIF_real1.tar.gz)
2. [USPTO_real1](https://github.com/jshmjs45/data_for_science/blob/master/data_for_practicality_judgment/USPTO_real1.tar.gz)
3. [CJHIF_rule](https://github.com/jshmjs45/data_for_science/blob/master/data_for_practicality_judgment/CJHIF_rule.tar.gz)
4. [USPTO_rule](https://github.com/jshmjs45/data_for_science/blob/master/data_for_practicality_judgment/USPTO_rule.tar.gz)

### 1.2.1 CJHIF_real1

| Case     | train     | dev     | test    |
| -------- | --------- | ------- | ------- |
| Positive | 1,406,259 | 156,251 | 173,624 |
| Negative | 7,178     | 798     | 874     |

### 1.2.2 USPTO_real1

| Case     | train     | dev     | test    |
| -------- | --------- | ------- | ------- |
| Positive | 217,992   | 24,221  | 26,919  |
| Negative | 7,176     | 797     | 877     |

### 1.2.3 CJHIF_rule

| Case     | train     | dev     | test    |
| -------- | --------- | ------- | ------- |
| Positive | 1,428,673 | 158,741 | 89,948  |
| Negative | 158,689   | 17,632  | 10,052  |

### 1.2.4 USPTO_rule

| Case     | train     | dev     | test    |
| -------- | --------- | ------- | ------- |
| Positive | 217,799   | 24,200  | 90,221  |
| Negative | 24,421    |2,713    | 9,779   |


# 2 codes\_for\_science
Code instruction accompanying the paper **"Chemical Reaction Practicality Judgment via Deep Symbol Artificial Intelligence"**

## 2.0 Requirments

These is no restriction on the system, like windows or linux.

The followings are runtime requirements:

python 2.7 or 3.6

keras 1.2.0

We strongly suggest you to use <code>[conda](https://www.anaconda.com/download/)</code> to control the virtual environment.

You can install the packages by `pip install package_name`.


## 2.1 Codes for data preprocessing
1. convert_file.py 
2. clear_file.py
3. select_file.py
4. combine_files.py

### 2.1.1 convert_file.py 
We canonicalize data without atom mappings by using this code.

The parameters are as follows:

**--mode** 0:CJHIF 1:USPTO 2:Chemical.AI

**--file** input file path

Usage: `python convert_file.py [--mode MODE] [--file FILE]`

### 2.1.2 clear_file.py 
The converted file is cleared by using this coede.

The parameters are as follows:

**--mode** 0:CJHIF 1:USPTO 2:Chemical.AI

**--file** input file path

Usage: `python clear_file.py [--mode MODE] [--file FILE]`

### 2.1.3 slelct_file.py 
The cleared file is split into train set and test set by using this code.

The parameters are as follows:

**--per** the ratio of the test set (%)

**--file** input file path

Usage: `python clear_file.py [--per PER] [--file FILE]`

### 2.1.4 combine_files.py

This code combines the positive data and negetive data and split the combined file into train set and test set. 

**--per** the ratio of the test set (%)

**--file1** positive file path

**--file2** negative file path

Usage: `python clear_file.py [--per PER] [--file1 FILE1] [--file2 FILE2]`






## 2.2 Data Formatting and Embedding Generating

After Unsupervised Tokenization and Reaction Step Generation, we use `myio.py` to format the input data to fed to the neural network.

In the output directory specified in `myio.py` (for example, `data/USPTO`), we obtain the formatted data vocabulary  with two folders, **train/** and **test/** which contain input sequences for training and evaluation . 

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

## 2.3 Practicality Judgment

For Practicality Judgment, we exectute `class_siamese_final.py`.

The parameters are as follows:

**--data**  the top directory of the processed data after data formatting (for example, `data/USPTO`)

**--folder** where you want to save the models and logs in each epoch

**--epochs** max epoch for training

**--dim** hidden dimmension for the Siamese Network

**--maxlen** the specified max length for input sequences (truncating or zero-padding when needed)

**--mode** 0 : using all features, 1: remove steps, 2: remove reaction conditions, 3: remove steps and conditions

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

If GPU is availble, then add the script in front: ``CUDA_VISIBLE_DEVICES = the GPU id
CUDA_VISIBLE_DEVICES = 0 python class_siamese_final.py --data data/USPTO_Rule --folder USPTO_Rule``

Then the terminal will show the training and evaluation results.
