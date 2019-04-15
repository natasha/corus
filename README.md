
# Links to russian corpora + python functions for loading and parsing

in one place

<!--- registry --->
<table>
<tr>
<th>Dataset</th>
<th>API <code>from corus import</code></th>
<th>Usage</th>
</tr>
<tr>
<td>
<a href="https://github.com/yutkin/Lenta.Ru-News-Dataset">Lenta.ru</a>
</td>
<td>
<code>load_lenta</code>
</td>
<td>
wget https://github.com/yutkin/Lenta.Ru-News-Dataset/releases/download/v1.0/lenta-ru-news.csv.gz
</br>
See <code>load_lenta</code> <a href="https://nbviewer.jupyter.org/github/natasha/corus/blob/master/docs.ipynb#lenta">usage example</a>
</td>
</tr>
<tr>
<td>
<a href="https://github.com/dialogue-evaluation/factRuEval-2016/">factRuEval-2016</a>
</td>
<td>
<code>load_factru</code>
</td>
<td>
wget https://github.com/dialogue-evaluation/factRuEval-2016/archive/master.zip
</br>
unzip master.zip
</br>
rm master.zip
</br>
See <code>load_factru</code> <a href="https://nbviewer.jupyter.org/github/natasha/corus/blob/master/docs.ipynb#factru">usage example</a>
</td>
</tr>
<tr>
<td>
<a href="https://www.researchgate.net/publication/262203599_Introducing_Baselines_for_Russian_Named_Entity_Recognition">Gareev</a>
</td>
<td>
<code>load_gareev</code>
</td>
<td>
Email Rinat Gareev (gareev-rm@yandex.ru) ask for dataset
</br>
tar -xvf rus-ner-news-corpus.iob.tar.gz
</br>
rm rus-ner-news-corpus.iob.tar.gz
</br>
See <code>load_gareev</code> <a href="https://nbviewer.jupyter.org/github/natasha/corus/blob/master/docs.ipynb#gareev">usage example</a>
</td>
</tr>
<tr>
<td>
<a href="http://www.labinform.ru/pub/named_entities/">Collection5</a>
</td>
<td>
<code>load_ne5</code>
</td>
<td>
wget http://www.labinform.ru/pub/named_entities/collection5.zip
</br>
unzip collection5.zip
</br>
rm collection5.zip
</br>
See <code>load_ne5</code> <a href="https://nbviewer.jupyter.org/github/natasha/corus/blob/master/docs.ipynb#ne5">usage example</a>
</td>
</tr>
<tr>
<td>
<a href="https://www.aclweb.org/anthology/I17-1042">WiNER</a>
</td>
<td>
<code>load_wikiner</code>
</td>
<td>
wget https://github.com/dice-group/FOX/raw/master/input/Wikiner/aij-wikiner-ru-wp3.bz2
</br>
See <code>load_wikiner</code> <a href="https://nbviewer.jupyter.org/github/natasha/corus/blob/master/docs.ipynb#wikiner">usage example</a>
</td>
</tr>
</table>
<!--- registry --->
