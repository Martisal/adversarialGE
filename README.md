# Introduction

This repository contains the files and instructions for replicating the experiments described in the paper 

C. Ferretti and M. Saletta. "*Deceiving Neural Source Code Classifiers: Finding Adversarial Examples with Grammatical Evolution*". In: GECCO '21: Genetic and Evolutionary Computation Conference, Companion Volume (SecDef Workshop), pages 1889-1897. 2021. 

The founding idea is to exploit the knowledge learned by machine learning systems dealing with source code for leading the evolution of programs that satisfy given specifications or bear certain properties. 

We first introduce the approach by providing a simple example in which the output of a perceptron trained to count the number of zeros in a binary string is used as the fitness function of a Grammatical Evolution algorithm; we then illustrate how to replicate all the experiments described in the referred paper, in which a similar approach is used for prodicing C programs able to deceive a neural vulnerability detector.   

# Examples

The experiments are all performed by using the [PonyGE2](https://github.com/PonyGE/PonyGE2) implementation of Grammatical Evolution, and on some machine learning platform, mainly used for inference on given instances.

# Reference

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



