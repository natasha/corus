
# Links to russian corpora + python functions for loading and parsing

in one place

<!--- registry --->
<table>
<tr>
<th>Dataset</th>
<th>API <code>from corus import</code></th>
<th>How to download</th>
</tr>
<tr>
<td>
<a href="https://github.com/yutkin/Lenta.Ru-News-Dataset">Lenta.ru</a>
</br>
Dump of lenta.ru, ~790 000 articles, ~1.9Gb of text.
</td>
<td>
<code>load_lenta</code>
</br>
<a href="https://nbviewer.jupyter.org/github/natasha/corus/blob/master/docs.ipynb#lenta">usage example</a>
</td>
<td>
wget https://github.com/yutkin/Lenta.Ru-News-Dataset/releases/download/v1.0/lenta-ru-news.csv.gz
</td>
</tr>
<tr>
<td>
<a href="https://github.com/dialogue-evaluation/factRuEval-2016/">factRuEval-2016</a>
</br>
254 news articles with PER, LOC, ORG markup.
</td>
<td>
<code>load_factru</code>
</br>
<a href="https://nbviewer.jupyter.org/github/natasha/corus/blob/master/docs.ipynb#factru">usage example</a>
</td>
<td>
wget https://github.com/dialogue-evaluation/factRuEval-2016/archive/master.zip
</br>
unzip master.zip
</br>
rm master.zip
</td>
</tr>
<tr>
<td>
<a href="https://www.researchgate.net/publication/262203599_Introducing_Baselines_for_Russian_Named_Entity_Recognition">Gareev</a>
</br>
97 news articles with PER, ORG markup.
</td>
<td>
<code>load_gareev</code>
</br>
<a href="https://nbviewer.jupyter.org/github/natasha/corus/blob/master/docs.ipynb#gareev">usage example</a>
</td>
<td>
Email Rinat Gareev (gareev-rm@yandex.ru) ask for dataset
</br>
tar -xvf rus-ner-news-corpus.iob.tar.gz
</br>
rm rus-ner-news-corpus.iob.tar.gz
</td>
</tr>
<tr>
<td>
<a href="http://www.labinform.ru/pub/named_entities/">Collection5</a>
</br>
1000 news articles with PER, LOC, ORG markup.
</td>
<td>
<code>load_ne5</code>
</br>
<a href="https://nbviewer.jupyter.org/github/natasha/corus/blob/master/docs.ipynb#ne5">usage example</a>
</td>
<td>
wget http://www.labinform.ru/pub/named_entities/collection5.zip
</br>
unzip collection5.zip
</br>
rm collection5.zip
</td>
</tr>
<tr>
<td>
<a href="https://www.aclweb.org/anthology/I17-1042">WiNER</a>
</br>
~200 000 sentences from Wiki automaticaly annotated with PER, LOC, ORG tags.
</td>
<td>
<code>load_wikiner</code>
</br>
<a href="https://nbviewer.jupyter.org/github/natasha/corus/blob/master/docs.ipynb#wikiner">usage example</a>
</td>
<td>
wget https://github.com/dice-group/FOX/raw/master/input/Wikiner/aij-wikiner-ru-wp3.bz2
</td>
</tr>
<tr>
<td>
<a href="https://russe.nlpub.org/downloads/">Lib.rus.ec</a>
</br>
Dump of lib.rus.ec, ~150Gb of text, prepared for RUSSE workshop.
</td>
<td>
<code>load_librusec</code>
</br>
<a href="https://nbviewer.jupyter.org/github/natasha/corus/blob/master/docs.ipynb#librusec">usage example</a>
</td>
<td>
wget http://panchenko.me/data/russe/librusec_fb2.plain.gz
</td>
</tr>
</table>
<!--- registry --->


## Development

Tests:

```bash
make test
```

Add new sourse:
1. Implement `corus/sources/<source>.py`
2. Add import and registy entry into `corus/__init__.py`
3. Add example into `docs.ipynb`
4. Run tests (readme is updated)
