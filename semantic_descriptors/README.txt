Created by: Ted Huang, Nov 29, 2015
Last revised: November 23, 2016

The goal of this program is to be able to find synonyms 
or words with close meaning, when given some word. 

This accomplished using a semantic descriptor tester.
One way to calculate if words are similar to one 
another is to calculate how many times they appear in the same sentence.

A semantic descriptor is a long dictionary of test words as keys. The 
content of each key is another dictionary with more words as keys and 
numbers as values. The number indicates how many times the two keys
(the test word and the one whose value is the number)
appear in the same sentence.

For example, if the semantic descriptor were
{.... "fly": {"chicken": 2,..... "bird": 3} .....}
then "fly" would have appeared in the same sentence as "bird" 3 times. 

To build a semantic descriptor, one would need a text file sufficiently
long such that it has enough words to work with to give acceptable results.

There is a score that represents the correlation
between two words, and that can be computed from many different formulas. 
This includes the cosine similarity and the Euclidean space formula.

The "test.txt" file is meant for the function "run_similarity_test", 
and all other text files are meant for building the semantic descriptor. 