
# Corus

Links to russian corpora + python functions for loading and parsing

<!--- metas --->
<table>
<tr>
<th>Dataset</th>
<th>API <code>from corus import</code></th>
<th>Description</th>
</tr>
<tr>
<td>
<a href="https://github.com/dialogue-evaluation/factRuEval-2016/">factRuEval-2016</a>
</td>
<td>
<code><a href="https://nbviewer.jupyter.org/github/natasha/corus/blob/master/docs.ipynb#load_factru">load_factru</a></code>
</td>
<td>
254 news articles with manual PER, LOC, ORG markup.
</br>
#ner
</br>
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
</td>
<td>
<code><a href="https://nbviewer.jupyter.org/github/natasha/corus/blob/master/docs.ipynb#load_gareev">load_gareev</a></code>
</td>
<td>
97 news articles with manual PER, ORG markup.
</br>
#ner
</br>
Email Rinat Gareev (gareev-rm@yandex.ru) ask for dataset
</br>
tar -xvf rus-ner-news-corpus.iob.tar.gz
</br>
rm rus-ner-news-corpus.iob.tar.gz
</td>
</tr>
<tr>
<td>
<a href="https://github.com/yutkin/Lenta.Ru-News-Dataset">Lenta.ru</a>
</td>
<td>
<code><a href="https://nbviewer.jupyter.org/github/natasha/corus/blob/master/docs.ipynb#load_lenta">load_lenta</a></code>
</td>
<td>
Dump of lenta.ru, ~790 000 articles, ~1.9Gb of text.
</br>
#news
</br>
wget https://github.com/yutkin/Lenta.Ru-News-Dataset/releases/download/v1.0/lenta-ru-news.csv.gz
</td>
</tr>
<tr>
<td>
<a href="https://russe.nlpub.org/downloads/">Lib.rus.ec</a>
</td>
<td>
<code><a href="https://nbviewer.jupyter.org/github/natasha/corus/blob/master/docs.ipynb#load_librusec">load_librusec</a></code>
</td>
<td>
Dump of lib.rus.ec prepared for RUSSE workshop, ~150Gb of text.
</br>
wget http://panchenko.me/data/russe/librusec_fb2.plain.gz
</td>
</tr>
<tr>
<td>
<a href="http://www.labinform.ru/pub/named_entities/">Collection5</a>
</td>
<td>
<code><a href="https://nbviewer.jupyter.org/github/natasha/corus/blob/master/docs.ipynb#load_ne5">load_ne5</a></code>
</td>
<td>
1000 news articles with manual PER, LOC, ORG markup.
</br>
#ner
</br>
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
</td>
<td>
<code><a href="https://nbviewer.jupyter.org/github/natasha/corus/blob/master/docs.ipynb#load_wikiner">load_wikiner</a></code>
</td>
<td>
~200 000 sentences from Wiki auto annotated with PER, LOC, ORG tags.
</br>
#ner
</br>
wget https://github.com/dice-group/FOX/raw/master/input/Wikiner/aij-wikiner-ru-wp3.bz2
</td>
</tr>
<tr>
<td>
<a href="https://tatianashavrina.github.io/taiga_site/">Taiga</a>
</td>
<td>
</td>
<td>
wget https://linghub.ru/static/Taiga/retagged_taiga.tar.gz
</br>
tar -xzvf retagged_taiga.tar.gz
</td>
</tr>
</table>
<!--- metas --->


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
