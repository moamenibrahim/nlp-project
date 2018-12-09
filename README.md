# Suomi24: Mining Health Discussions

Text mining and analysis on health discussions on [suomi24](https://www.suomi24.fi/).

## About the project

This project concerns a rough exploration of the Finnish Suomi24 dataset in order to map the discussions related to health, answering the questions: What are the main health issues that much interest citizens? What are their key worries, inspirations? How such worries, inspirations are manifested in the forum?

## Requirements

* virtualenv
* python3
* java
* download stanford named entity taggger and unzip it in stanford folder: [stanford-ner-2018-10-16](https://nlp.stanford.edu/software/stanford-ner-2018-10-16.zip)

## Getting Started

Clone the Repository
As usual, you get started by cloning the project to your local machine:

```bash
git clone git@github.com:moamenibrahim/nlp_project.git
cd nlp_project/
```

Create a virtual enviroment in the current project folder using python3

```bash
virtualenv -p python3 venv
source venv/bin/activate
pip install -r requirements.txt
./init.sh
```

### To apply sentiment analysis on Finnish text using sentiment tagged list of words

Clone refined afinn repository to work on Finnish text

```bash
git clone git@github.com:moamenibrahim/afinn.git
cd afinn/
```

Install afinn using activated virtualenv then return to main repo folder

```bash
python setup.py build
python setup.py install
cd ..
```

## Authors

* Moamen Ibrahim
* [Sercan Türkmen](https://github.com/sercant/)
* Mina Maged
* Matti Eteläperä
