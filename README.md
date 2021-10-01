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

The aim is to evolve binary strings having the highest possible of zeros. Notice that, for this simple task, a conventional fitnenss function that counts the zeros, as the one in `./fitness/zeromax.py`, should be sufficient. However, since we are interested in exploiting the activation of artificial neurons for computing the fitness, for this example we use the output of a multilayer perceptron trained in counting the number of zeros in the string. For training a new model trying different parameters, just modify and run the script `perceptron_zeromax.py`.

This example requires:

* Grammar file: `./grammars/example01.bnf`
* Parameters file: `./parameters/example01.txt`
* Neural model: `./models/mlp_zeromax.pickle`
* Fitness function: `./fitness/zeromax_neuro.py`

Be sure that all these files are properly located in the sub-directories of PonyGE2, as explained in the previous section.

For running this example, just run `python ponyge.py --parameters example01.txt`

## Adversarial approach: C Programs

## Customized examples

# References

<a id="1">[1]</a> C. Ferretti and M. Saletta. "*Deceiving Neural Source Code Classifiers: Finding Adversarial Examples with Grammatical Evolution*". In: GECCO '21: Genetic and Evolutionary Computation Conference, Companion Volume (SecDef Workshop), pp. 1889-1897. 2021. 

<a id="2">[2]</a> M. O’Neill and C. Ryan. "*Grammatical evolution*". In: IEEE Trans. Evol. Comput.5(4), pp. 349–358. 2001.

<a id="3">[3]</a>  R.L. Russell et al. "*Automated vulnerability detection in source code using deep representation learning*". In: Proceedings of 17th IEEE International Conference on Machine Learning and Applications, ICMLA. pp. 757–762. 2018.

# Citation

If you find this repository useful for your work, please cite us:

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



