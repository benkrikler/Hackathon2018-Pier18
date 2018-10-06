#! /bin/bash

virtualenv stanfordNLP
source stanfordNLP/bin/activate

pip install nltk
python -c "import nltk as mod;print mod.__file__"

mkdir stanfordNLP-models
cd stanfordNLP-model
wget https://nlp.stanford.edu/software/stanford-ner-2018-02-27.zip
unzip stanford-ner-2018-02-27.zip

cd stanford-ner-2018-02-27
export CLASSPATH=$PWD
export STANFORD_MODELS=$PWD/classifiers/

python -c "from nltk.tag import StanfordNERTagger;st = StanfordNERTagger('english.all.3class.distsim.crf.ser.gz');st.tag('Rami Eid is studying at Stony Brook University in NY'.split())"
python -c "from nltk.tag import StanfordNERTagger;st = StanfordNERTagger('english.muc.7class.distsim.crf.ser.gz');print st.tag('Rami Eid is studying at Stony Brook University in NY in July at the UN'.split())"
