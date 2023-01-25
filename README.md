# jupyter-duplicates-analysis

## Getting started

In order to start using the study, 
it is necessary to unpack the data and install the necessary environment.

To install all the necessary environment, use
```
 poetry install
```

After that, you can unpack the archives with the data
```python
from utils.data_utils import unzip_data

unzip_data('data/in/')
unzip_data('data/out/')
```

## Clones analysis

The whole experiment consists of several stages: 
1. Aggregation and filtering of clone data
2. Data transform to probabilistic distribution
3. Random variables analysis

### Aggregation and filtering
Each of the clone results files contains some meta information about the file and a list of groups of found clones, 
with a minimum clone length of 3. At the aggregation and filtering stage, the number of clones is filtered for each 
individual results file by their minimum length. Thus, after filtering, one file corresponds to a certain functional 
dependence of the number of clones on the minimum allowable clone length. Further, this information is aggregated for all files. 
Also, at the filtering stage, it is possible to prohibit the separator presenting in the duplicate, 
which makes sense, for example, to ban those duplicates that are in several cells of the notebook at once.
It is also possible to pre-normalize the number of clones to the full length of PSI

### Data transform to probabilistic distribution
After aggregating the number of clones, we can consider the resulting data as the distribution of the number 
of clones for each minimum clone length. Next, we find the average of the distribution corresponding to each of 
the minimum length of the duplicate and thus obtain a single functional dependence for all - the average number 
of clones from the minimum length of the duplicate. 

We further transform the resulting functional dependence into a distribution mass function by normalization.
It turns out that we were able to reduce two sets of data corresponding to different environments to some 
discrete random variables, which we will eventually compare with each other.

$$\{(\text{Clones count}, \text{Minimum clone length}_j)_i \; | \; i = 1 ..N_{files}, j = 3..M\} \to$$

$$\to \{(\text{Minimum clone length}_j, \{\text{Clone count}_i \; | \; i = 1..N_{files} \}) \; | \; i = 1 ..N_{files}, j = 3..M\}$$

$$\to \{(\text{Minimum clone length}_j, \text{Mean clones count}_j \; | \; j = 3..M\} \sim F(\text{Minimum clone length})$$

$$F(\text{Minimum clone length}) \to \frac{F(\text{Minimum clone length})}{\text{normalization factor}}$$

### Random variables analysis
To compare random variables, initially we sample 10000 values of each of them. 
The initial condition of our study is some allocated minimum duplicate length 
(for example, in our case 45 units for scripts). Our task is to find the appropriate value for notebooks. 
We decided to do this using quantile analysis of a random variable. We can find the corresponding quantile rank 
corresponding to the selected value in scripts, this quantile-rank is essentially cumulative density function (CDF) of this value.
Next, it remains for us to find the corresponding quantile in the notebooks. 
Mathematically, this can be described as follows:

$$\theta_{scripts} = 45 \to CDF_{scripts}(\theta_{scripts}) = p_{scripts}$$

$$CDF_{notebooks}^{-1} (p_{scripts}) = \theta_{notebooks}$$

### Example of usage
```python
from pathlib import Path
from experiment import Experiment

notebooks_path = Path('data/out/notebooks_data')
scripts_path = Path('data/out/scripts_data')

e = Experiment(
    notebooks_folder=notebooks_path,
    scripts_folder=scripts_path,
    max_num=10_000
)

min_clone_length, max_clone_length = 3, 90
e.run(normalize=False, drop_breaks=False, length_range=range(3, max_clone_length + 1))
```
