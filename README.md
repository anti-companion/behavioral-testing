# Behavioral testing
Wait, what the hell is behavioral testing?

BH is a way to systematically test NLP models by testing their,  ...well - behavior. For example, we would like to check if a sentiment prediction model makes any assumption for the movie's origin country. So we define a template:

The movie was produced in COUNTRY. It is a [remaining of the review]

And run multiple tests by substituting COUNTRY with different values (USA, Germany, Italy, Turkey, China, etc.). Then, we collect model predictions and evaluate if they are consistent (preds for equal review with only COUNTRY changed are similar) or if a model decides that movies from specific regions are worse than others.

For a generative model, we can quickly check if it, e.g.: correctly remembers its identity or memories. 

# This repo

This repo contains code for performing such tests for various models. It is intended to be as automatic as possible, so those tests can be run to check if there are regression bugs or quickly validate if another model is better/worse.
