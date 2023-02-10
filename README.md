# The Hot Hand Fallacy - a Markovic Point of View

[![HitCount](https://hits.dwyl.com/menisadi/markovic-hot-hand.svg?style=flat-square)](http://hits.dwyl.com/menisadi/markovic-hot-hand)

![banner](graphics/basketball.png)

## Introduction

The hot hand fallacy is a popular basketball myth that suggests that a player is more likely to score a basket if they have made several shots in a row. This project takes data of shots by NBA stars and applies statistical tools to check if this phenomenon is indeed real or simply a result of plain randomness and the law of large numbers. The analysis focuses on modeling the process as a Markov chain, meaning that each shot's success probability depends on past shots. The main idea is to calculate those dependencies and their magnitude.

## Data

The data used in this project is a collection of shots taken by NBA players during the 2018-2019 season. The data includes information such as the player's name, the game they played in, the shot type, the outcome of the shot (made or missed), and the number of consecutive made shots prior to that shot.

## Methodology

The project is done using python, numpy, pandas, and scipy. The first step is to clean and prepare the data for analysis. This involves removing missing values and converting relevant columns into the appropriate data type. Next, the dependencies between shots are calculated using a Markov chain model. The probabilities of making a shot given a certain number of consecutive made shots are estimated and visualized. Finally, a statistical test is performed to determine if there is a significant difference between the observed data and a model that assumes that the shots are independent and identically distributed.

## Results

The results of this project will provide insight into whether or not the hot hand fallacy is a real phenomenon in the NBA. If the hot hand effect is found to be real, the magnitude of the effect will also be estimated. These results will be presented in the form of visualizations and statistical tests.

## Conclusion

The results of this project will contribute to the ongoing debate on the hot hand fallacy and provide a fresh perspective using Markov chain models. The findings of this project will be of interest to basketball fans, statisticians, and researchers who are interested in understanding the underlying process behind

## How to Cite
If you use this project in your research or work, please cite it as follows:
```
@misc{markovic_hot_hand_analysis,
  author = {Dvir Ross, Menachem Sadigurschi, Inbar Tamir},
  title = {The Hot Hand Fallacy - a Markovic Point of View},
  year = {2023},
  howpublished = {\url{https://github.com/menisadi/markovic-hot-hand}}
}
```
