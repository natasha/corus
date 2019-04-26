
# Corus

Links to russian corpora + python functions for loading and parsing

<!--- metas --->
<table>
<tr>
<th>Dataset</th>
<th>API <code>from corus import</code></th>
<th>Tags</th>
<th>Records</th>
<th>Uncompressed, Mb</th>
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
#ner
#news
</td>
<td>
254
</td>
<td>
0.95
</td>
<td>
Manual PER, LOC, ORG markup prepared for 2016 Dialog competition.
</br>
</br>
<code>wget https://github.com/dialogue-evaluation/factRuEval-2016/archive/master.zip</code>
</br>
<code>unzip master.zip</code>
</br>
<code>rm master.zip</code>
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
#ner
#news
</td>
<td>
97
</td>
<td>
0.44
</td>
<td>
Manual PER, ORG markup.
</br>
</br>
Email Rinat Gareev (gareev-rm@yandex.ru) ask for dataset
</br>
<code>tar -xvf rus-ner-news-corpus.iob.tar.gz</code>
</br>
<code>rm rus-ner-news-corpus.iob.tar.gz</code>
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
#news
</td>
<td>
739 351
</td>
<td>
1 702
</td>
<td>
Dump of lenta.ru
</br>
</br>
<code>wget https://github.com/yutkin/Lenta.Ru-News-Dataset/releases/download/v1.0/lenta-ru-news.csv.gz</code>
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
#lit
</td>
<td>
301 871
</td>
<td>
148 402
</td>
<td>
Dump of lib.rus.ec prepared for RUSSE workshop
</br>
</br>
<code>wget http://panchenko.me/data/russe/librusec_fb2.plain.gz</code>
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
#ner
#news
</td>
<td>
1 000
</td>
<td>
2
</td>
<td>
News articles with manual PER, LOC, ORG markup.
</br>
</br>
<code>wget http://www.labinform.ru/pub/named_entities/collection5.zip</code>
</br>
<code>unzip collection5.zip</code>
</br>
<code>rm collection5.zip</code>
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
#ner
</td>
<td>
203 287
</td>
<td>
36
</td>
<td>
Sentences from Wiki auto annotated with PER, LOC, ORG tags.
</br>
</br>
<code>wget https://github.com/dice-group/FOX/raw/master/input/Wikiner/aij-wikiner-ru-wp3.bz2</code>
</td>
</tr>
<tr>
<td>
<a href="https://tatianashavrina.github.io/taiga_site/">Taiga</a>
</td>
<td>
</td>
<td>
</td>
<td>
</td>
<td>
</td>
<td>
Large collection of russian texts from various sources: news sites, magazines, literacy, social networks.
</br>
</br>
<code>wget https://linghub.ru/static/Taiga/retagged_taiga.tar.gz</code>
</br>
<code>tar -xzvf retagged_taiga.tar.gz</code>
</td>
</tr>
<tr>
<td>
Taiga/Arzamas
</td>
<td>
<code><a href="https://nbviewer.jupyter.org/github/natasha/corus/blob/master/docs.ipynb#load_taiga_arzamas">load_taiga_arzamas</a></code>
</td>
<td>
#news
</td>
<td>
311
</td>
<td>
4
</td>
<td>
Dump of arzamas.academy.
</td>
</tr>
<tr>
<td>
Taiga/Fontanka
</td>
<td>
<code><a href="https://nbviewer.jupyter.org/github/natasha/corus/blob/master/docs.ipynb#load_taiga_fontanka">load_taiga_fontanka</a></code>
</td>
<td>
#news
</td>
<td>
342 683
</td>
<td>
786
</td>
<td>
Dump of fontanka.ru.
</td>
</tr>
<tr>
<td>
Taiga/Interfax
</td>
<td>
<code><a href="https://nbviewer.jupyter.org/github/natasha/corus/blob/master/docs.ipynb#load_taiga_interfax">load_taiga_interfax</a></code>
</td>
<td>
#news
</td>
<td>
46 429
</td>
<td>
77
</td>
<td>
Dump of interfax.ru.
</td>
</tr>
<tr>
<td>
Taiga/KP
</td>
<td>
<code><a href="https://nbviewer.jupyter.org/github/natasha/corus/blob/master/docs.ipynb#load_taiga_kp">load_taiga_kp</a></code>
</td>
<td>
#news
</td>
<td>
45 503
</td>
<td>
61
</td>
<td>
Dump of kp.ru.
</td>
</tr>
<tr>
<td>
Taiga/Lenta
</td>
<td>
<code><a href="https://nbviewer.jupyter.org/github/natasha/corus/blob/master/docs.ipynb#load_taiga_lenta">load_taiga_lenta</a></code>
</td>
<td>
#news
</td>
<td>
36 446
</td>
<td>
95
</td>
<td>
Dump of lenta.ru.
</td>
</tr>
<tr>
<td>
Taiga/N+1
</td>
<td>
<code><a href="https://nbviewer.jupyter.org/github/natasha/corus/blob/master/docs.ipynb#load_taiga_nplus1">load_taiga_nplus1</a></code>
</td>
<td>
#news
</td>
<td>
7 696
</td>
<td>
24
</td>
<td>
Dump of nplus1.ru.
</td>
</tr>
<tr>
<td>
Taiga/Magazines
</td>
<td>
<code><a href="https://nbviewer.jupyter.org/github/natasha/corus/blob/master/docs.ipynb#load_taiga_magazines">load_taiga_magazines</a></code>
</td>
<td>
</td>
<td>
39 890
</td>
<td>
2 243
</td>
<td>
Dump of magazines.russ.ru
</td>
</tr>
<tr>
<td>
Taiga/Subtitles
</td>
<td>
<code><a href="https://nbviewer.jupyter.org/github/natasha/corus/blob/master/docs.ipynb#load_taiga_subtitles">load_taiga_subtitles</a></code>
</td>
<td>
</td>
<td>
19 011
</td>
<td>
909
</td>
<td>
</td>
</tr>
<tr>
<td>
Taiga/Social
</td>
<td>
<code><a href="https://nbviewer.jupyter.org/github/natasha/corus/blob/master/docs.ipynb#load_taiga_social">load_taiga_social</a></code>
</td>
<td>
</td>
<td>
1 876 442
</td>
<td>
648
</td>
<td>
</td>
</tr>
<tr>
<td>
Taiga/Proza
</td>
<td>
<code><a href="https://nbviewer.jupyter.org/github/natasha/corus/blob/master/docs.ipynb#load_taiga_proza">load_taiga_proza</a></code>
</td>
<td>
#lit
</td>
<td>
1 732 434
</td>
<td>
39 164
</td>
<td>
Dump of proza.ru
</td>
</tr>
<tr>
<td>
Taiga/Stihi
</td>
<td>
<code><a href="https://nbviewer.jupyter.org/github/natasha/corus/blob/master/docs.ipynb#load_taiga_stihi">load_taiga_stihi</a></code>
</td>
<td>
</td>
<td>
9 157 686
</td>
<td>
13 109
</td>
<td>
Dump of stihi.ru
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
