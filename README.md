# 1 data\_for\_science
Data for our paper "Chemical Reaction Practicality Judgment via Deep Symbol Artificial Intelligence".

 1. [original_data](https://github.com/jshmjs45/data_for_science/tree/master/original_data)
 2. [data\\_for\\_practicality\\_judgment](https://github.com/jshmjs45/data_for_science/tree/master/data_for_practicality_judgment)

All files are encoded in UTF-8 without Byte Order Mark (BOM).

## 1.1 original\_data
This zipped file includes three files:

1. [data\\_from\\_USPTO\\_utf8](https://github.com/jshmjs45/data_for_science/blob/master/original_data/data_from_USPTO_utf8.tar.gz)
2. [data\\_from\\_CJHIF\\_utf8](https://github.com/jshmjs45/data_for_science/blob/master/original_data/data_from_CJHIF_utf8.tar.gz)
3. [data\\_from\\_ChemicalAI\\_Rule\\_utf8](https://github.com/jshmjs45/data_for_science/blob/master/original_data/data_from_ChemicalAI_Rule_utf8.tar.gz)
4. [data\\_from\\_ChemicalAI\\_Real\\_1\\_utf8](https://github.com/jshmjs45/data_for_science/blob/master/original_data/data_from_ChemicalAI_Real_1_utf8.tar.gz)
5. [data\\_from\\_ChemicalAI\\_Real\\_2\\_utf8](https://github.com/jshmjs45/data_for_science/blob/master/original_data/data_from_ChemicalAI_Real_2_utf8.tar.gz)


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
### 1.2.1 CJHIF_real1

| Case     | train     | dev     | test    |
| -------- | --------- | ------- | ------- |
| Positive | 1,406,259 | 156,251 | 173,624 |
| Negative | 7,178     | 798     | 874     |

### 1.2.2 USPTO_real1
### 1.2.3 CJHIF_rule
### 1.2.4 USPTO_rule
