# Introduction

This repository contains the files and instructions for replicating the experiments described in [[1]](#1).  

The founding idea is to exploit the knowledge learned by machine learning systems dealing with source code for leading the evolution of programs that satisfy given specifications or bear certain properties. 

We first introduce the approach by providing a simple example in which the output of a perceptron trained to count the number of zeros in a binary string is used as the fitness function of a Grammatical Evolution (GE) [[2]](#2) algorithm; we then illustrate how to replicate all the experiments described in the referred paper, in which a similar approach is used for evolving C programs able to deceive a neural vulnerability detector.   

# Examples

The experiments are all performed by using the [PonyGE2](https://github.com/PonyGE/PonyGE2) implementation of Grammatical Evolution and external neural models for computing the fitness of the evolved individuals.

In general, for running all the examples, the steps are:

1. Clone the PonyGE2 repository, following the related [instructions](https://github.com/PonyGE/PonyGE2/wiki)
2. For each experiment:
    * Copy the appropriate fitness function in the `~/.../PonyGE2/src/fitness` directory
    * Copy the appropriate parameters file in the `~/.../PonyGE2/parameters` directory
    * Copy the appropriate grammar file in the `~/.../PonyGE2/grammars` directory
    * Modify the fitness function file so that the model for the inference is correctly referred
3. Run the experiment    

## Binary strings

This simple example is designed for becoming familiar with the approach and the interaction among the involved elements (namely, genetic algorithms, neural models, formal grammars). 

The aim is to evolve binary strings having the highest possible of zeros. Notice that, for this simple task, a conventional fitness function that counts the zeros, as the one in `./fitness/zeromax.py`, should be sufficient. However, since we are interested in exploiting the activation of artificial neurons for computing the fitness, for this example we use the output of a multilayer perceptron trained in counting the number of zeros in the string. For training a new model trying different parameters, just modify and run the script `perceptron_zeromax.py`.

This example requires:

* Grammar file: `./grammars/example01.bnf`
* Parameters file: `./parameters/example01.txt`
* Neural model: `./models/mlp_zeromax.pickle`
* Fitness function: `./fitness/zeromax_neuro.py`

Be sure that all these files are properly located in the sub-directories of PonyGE2, as explained in the previous section.

For running this example just run, from the home directory of PonyGE2: 
```
python ponyge.py --parameters example01.txt
```

## Adversarial approach: C Programs

This section describes how to replicate the experiments described in [[1]](#1). Specifically, we applied our approach by using, for computing the fitness function, the source code classifier proposed in [[3]](#3), which is a deep neural model trained in the detection and recognition of software vulnerabilities.

In these experiments, we are interested in evolving C program instances able to deceive such classifier, i.e. in taking the model to mislead the classification. To this aim, we propose two techniques:

1. The evolution of generic C programs that are arbitrarily classified as vulnerable or safe. For consistency with the paper, we will refer to these as *pure* individuals
2. The evolution of C statements to be injected in a given program after the return statement so to invert its original classification. We will refer to these as *hybrid* individuals

### Parameters

In all the experiments we propose, the considered grammar is `./grammars/EXcS.bnf`, which is a simplified C grammar that, differently from the original C programming language, contains only a subset of the operators, statements and library functions among its allowed productions.

The parameters for PonyGE2 specify the name of the grammar file and of the fitness function, besides other parameters controlling the evolutionary dynamics. They can be specified by modifying the file `./parameters/EXc.txt`:

    CACHE:                  False
    CODON_SIZE:             100000
    CROSSOVER:              variable_onepoint
    CROSSOVER_PROBABILITY:  0.75
    DEBUG:                  False
    GENERATIONS:            33
    MAX_GENOME_LENGTH:      5000
    GRAMMAR_FILE:           EXcS.bnf
    INITIALISATION:         uniform_tree
    INVALID_SELECTION:      False
    MAX_INIT_TREE_DEPTH:    10
    MAX_TREE_DEPTH:         30
    MUTATION:               int_flip_per_codon
    POPULATION_SIZE:        30
    FITNESS_FUNCTION:       activation_PURE
    REPLACEMENT:            generational
    SELECTION:              tournament
    TOURNAMENT_SIZE:        3
    VERBOSE:                True
    ELITE_SIZE:             1
    SAVE_ALL:               True

For convenience, each PonyGE2 session can be launched with an experiment name:

    python ponyge.py --parameters EXc.txt --experiment_name ExNm

The (one line) code of evolved individuals can be extracted from the session files, after the specified 33 generations, with commands such as:

    fgrep -A1 Phenotype /PATH_LEADING_TO/PonyGE2/results/ExNm/*/33.txt|fgrep txt-  

###  Fitness and neural models 

We provide three versions of the Python fitness file:

1. The first [one](./fitness/activation_PURE.py) corresponding to our experiments with evolving *pure* C-language individuals, i.e. source code individuals which are directly fed to the neural network;
2. a [second](./fitness/activation_INJECT.py) one reproducing our experiment that consists in modifying the source code of some labeled C-language instance by *injecting* evolved individuals after the return statement, just before the final closing bracket, so to preserve its body and its original behavior. Notice that this kind of semantic-preserving injection is reliable only in functions having a return statement, therefore we discourage the application of this approach for void C functions; 
3. a [template](./fitness/activation_TEMPLATE.py) version of the previous one, in which the selected C function to be modified with injections can be easily customized.

To run these specific fitness files, 2 files describing the trained neural network are required:

* a dump of the whole trained net, such as our provided `./models/model-epoch-100-04-single.hdf5`, working on the tensorflow platform,
* a snapshot of the tokenizer used to map the parse input to instance vectors, in our case the file `./tokenizer.pickle`.

The required libraries, in addition to PonyGE2, are related neural computations, C parsing, and serialization and can be easily installed with:

    pip install -r requirements.txt

The Python files representing the fitness functions have two main parts: the opening section performs all one-time operations, while the main function, is invoked to evaluate each individual, and we do this by parsing, tokenizing, and feeding it to the network, so to infer a prediction, finally returned by the function as the fitness of the given individual.

# References

<a id="1">[1]</a> C. Ferretti and M. Saletta. "*Deceiving Neural Source Code Classifiers: Finding Adversarial Examples with Grammatical Evolution*". In: GECCO '21: Genetic and Evolutionary Computation Conference, Companion Volume (SecDef Workshop), pp. 1889-1897. 2021. 

<a id="2">[2]</a> M. O’Neill and C. Ryan. "*Grammatical evolution*". In: IEEE Trans. Evol. Comput.5(4), pp. 349–358. 2001.

<a id="3">[3]</a>  R.L. Russell et al. "*Automated vulnerability detection in source code using deep representation learning*". In: Proceedings of 17th IEEE International Conference on Machine Learning and Applications, ICMLA. pp. 757–762. 2018.

# Citation

If you find this repository useful for your work, please include the following citation:

```
@inproceedings{adversarialGE,
  author    = {Claudio Ferretti and Martina Saletta},
  title     = {Deceiving neural source code classifiers: finding adversarial examples with grammatical evolution},
  booktitle = {{GECCO} '21: Genetic and Evolutionary Computation Conference, Companion Volume},
  pages     = {1889--1897},
  publisher = {{ACM}},
  year      = {2021},
}
```



