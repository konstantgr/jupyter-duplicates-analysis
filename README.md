# jupyter-duplicates-analysis

## Getting started

In order to replicate the study and inspect the results,
it is necessary to download and unpack the data,
and set up the environment.

### Setting up the environment

To set up the environment, use

```
poetry install
```

### Setting up the data

You can download data from zenodo: LINK

Then place the archives `archive_in` and `archive_in` in `'data'` folder and unpack the archives 
using `unzip_data`  method:

```python
from utils.data_utils import unzip_data
unzip_data('data')
```

## Clones analysis

The experiment consists of several stages:

0. Deduplication
1. Aggregation and filtering clone data
2. Building probabilistic distribution
3. Empirical analysis

### Deduplication

Search for duplicates was made using our suffix-tree algorithm for PSI. We used Lupa in order to automate deduplication
process. For each deduplicated file we got .json file which contains meta information about the processed file and a 
list of groups of found clones in it, with a minimum clone length of 3.

### Aggregation and filtering

At first step, for each file we arrange all found clones in groups with every 
possible minial threshold. Next we aggregate data from this groups across all files into one dataset which allows us to 
build minimal threshold amount to amount of clones distribution. 

Also, at this step it is possible to filter some clones. For example, we prohibit the separator presenting in the duplicate.
It allows to filter out duplicates that are in several cells of the notebook at once.
It is also possible to pre-normalize the number of clones to the full length of PSI,
however we don't use this feature in the study.

### Data transform to probabilistic distribution

After aggregating the clone data, we get distribution of the number
of clones for each minimum clone length. Next, we find the average of the distribution corresponding to each of
the minimum length of the duplicate and thus obtain a single functional dependence for all - the average number
of clones to the minimum length of the duplicate.

We further transform the resulting functional dependence into a distribution mass function by normalization.
It turns out that we are able to reduce two sets of data corresponding to different environments to some
discrete random variables, which we will compare with each other.

$$\{(\text{Clones count}, \text{Minimum clone length}_j)_i \; | \; i = 1 ..N_{files}, j = 3..M\} \to$$

$$\to \{(\text{Minimum clone length}_j, \{\text{Clone count}_i \; | \; i = 1..N_{files} \}) \; | \; i = 1 ..N_{files}, j = 3..M\}$$

$$\to \{(\text{Minimum clone length}_j, \text{Mean clones count}_j \; | \; j = 3..M\} \sim F(\text{Minimum clone length})$$

$$F(\text{Minimum clone length}) \to \frac{F(\text{Minimum clone length})}{\text{normalization factor}}$$

### Empirical analysis

In PyCharm default value for minimal size for highlight is 45 units of PSI tree. 
Our task is to find the optimal value for our notebook products -- Datalore and DataSpell.
We decided to do look for optimal corresponding value using quantile analysis. 
To compare clones in Python scripts and notebooks, we sampled 10000 values of each of them and calculated 
distribution of minial clone sizes to amount of clones.


The idea of analysis consists of two steps:
1) we can find the quantile rank corresponding to the given optimal value in scripts -- this quantile-rank is essentially cumulative density function (CDF) of
this value.
2) Next, it remains for us to find the corresponding quantile in the notebooks and infer its value in 
terms of PSI tree units.

Mathematically, this can be described as follows:

$$\theta_{scripts} = 45 \to CDF_{scripts}(\theta_{scripts}) = p_{scripts}$$

$$CDF_{notebooks}^{-1} (p_{scripts}) = \theta_{notebooks}$$

All code and examples could be found in the `clones-study.ipynb` notebook.
