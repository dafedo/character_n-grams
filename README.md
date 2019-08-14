# Character N-grams and Entropy

This repo contains code to:

* convert each text corpus into a linear sequence of character n-grams
(up to n = 4: unigrams, bigrams, trigrams and fourgrams);

* calculate probability distribution over the symbols of the
alphabet given a particular history; 

* compute the entropy of the probability distributions. 

Character n-gram distributions are investigated in two languages: English and German.
</br>
</br>
To run the code 
</br>
`python character_ngrams_probdist_&_entropy.py`
</br>
</br>
The program will produce the following plots
</br>
</br>
**Probability Distribution of Characters in the German Language by Growing History**
</br>
![No History](1.1.prob_dist_no_history.png)
</br>
![History = n](1.2.prob_dist_n_history.png)
</br>
![History = un](1.3.prob_dist_un_history.png)
</br>
![History = ung](1.4.prob_dist_gun_history.png)
</br>
</br>
</br>
**Bigram Probability Distribution of Characters in the German Language Given the History 'a', 'd', 'z' and 'c'.**
</br>
![History = a](2.1.prob_dist_a_history.png)
</br>
![History = d](2.2.prob_dist_d_history.png)
</br>
![History = z](2.3.prob_dist_z_history.png)
</br>
![History = c](2.4.prob_dist_c_history.png) 
</br>
</br>
</br>
**Entropy for N-gram Distributions of Different N-gram Size**
| History | No History | History = n | History = un | History = gun |
|---------|------------|-------------|--------------|---------------|
| Entropy | 4.182173   | 3.588221    | 1.766463     | 0.170460      |
</br>
</br>
</br>
**Entropy for Bigram Probability Distributions**
| History | History = a   | History = d   | History =  z  | History =  c  |
|---------|---------------|---------------|---------------|---------------|
| Entropy | 3.757168      | 2.056076      | 2.745905      | 0.826241      |
</br>
</br>
</br>
**15 the most frequent character unigrams, bigrams, trigrams, and fourgrams in the English and German corpora**
</br>
![15 the most frequent character ngrams](top_15_ngrams.png)
</br>