# Coreference resolution in NLP with AllenNLP and Huggingface 

:information_source: More theoretical background supported by examples can be found in our [introductory blog post](https://neurosys.com/article/intro-to-coreference-resolution-in-nlp/).  

:hugs: More details about **the most popular coreference resolution libraries** (followed by their strengths, weaknesses, and problems) can be found in our [second blog article](https://neurosys.com/article/most-popular-frameworks-for-coreference-resolution/).

:ok_hand: Some ideas concerning mentioned libraries and **improvements upon AllenNLP and Huggingface solutions** are described in detail in our [last blog post](https://neurosys.com/article/how-to-make-an-effective-coreference-resolution-model/).


## What is coreference resolution 
Coreference resolution (CR) is an NLP task that aims to group expressions referring to the same real-world entity to acquire less ambiguous text. It can be very useful in such tasks as text understanding, information extraction, summarization, or question answering. 

## Most popular CR libraries
We provide Jupyter notebooks showing the most basic usage of `Huggingface NeuralCoref` and `Allen Institute (AllenNLP)` coreference resolution models.  
:arrow_right: `huggingface_neuralcoref.ipynb`  
:arrow_right: `allennlp_coreference_resolution.ipynb`

More details about the models and some of their most common problems can be found in our [second blog post](https://neurosys.com/article/most-popular-frameworks-for-coreference-resolution/).

### Installation
We've encountered some difficulties during the installation of both libraries in a single Python/Conda environment. However, finally, we've come up with the setting which seems to work for our needs:
```python
pip install spacy==2.1.0
python -m spacy download en_core_web_sm
pip install neuralcoref --no-binary neuralcoref
pip install allennlp
pip install --pre allennlp-models
```
We consider the smallest `spaCy` model (`en_core_web_sm`) sufficient and not deviating from larger models but feel free to download whatever model seems best for you.


## Improvements upon the libraries
We've encountered several problems with clusters resolving in a text (the last step of replacing found mentions). As `AllenNLP` seems to find more suitable clusters (makes significantly fewer mistakes), we've decided to focus on this model. That's why we propose several improvements regarding its `replace_corefs` method.

:arrow_right: More details are provided by the `improvements_to_allennlp_cr.ipynb` notebook.

However, we still believe that `Huggingface NeuralCoref` is a valuable model that serves great as a reference. That's why we came up with a couple of intersection strategies - simply an ensemble of both models' outputs (clusters).   

:arrow_right: Their implementation and usage can be found in the `intersection_strategies.ipynb`.

## References
We're using the two most popular coreference resolution libraries: `Huggingface NeuralCoref` and `AllenNLP` implementation of `CorefResolver`.

| Implementation | Description | License |
|----------------|-------------|---------|
[Huggingface NeuralCoref 4.0](https://github.com/huggingface/neuralcoref) | It's a CR extension for [`spaCy`](https://spacy.io/) - very popular NLP library. `NeuralCoref` resolves coreference clusters using neural networks. More information can be found on their [blog post](https://medium.com/huggingface/state-of-the-art-neural-coreference-resolution-for-chatbots-3302365dcf30) and the [demo](https://huggingface.co/coref/). | [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)  <img width=250/> 
[AllenNLP coreference resolution](https://github.com/allenai/allennlp-models) | It's an open-source project being a part of [AI2](https://allenai.org/) institute which introduced e.g. [ELMo](https://allennlp.org/elmo). Their span-ranking coreference resolution model is also premised upon a neural model. More information is provided by their [demo](https://demo.allennlp.org/coreference-resolution). | [![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)  <img width=250/> 


