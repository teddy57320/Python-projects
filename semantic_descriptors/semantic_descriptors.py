# This is a semantic descriptor tester, which is used to find words of similar 
# meaning to a given word. One way to calculate if words are similar to one 
# another is to calculate how many times they appear in the same sentence.

# A semantic descriptor is a long dictionary of test words as keys with 
# another dictionary as its value. The inner dictionary contains words as keys
# and numbers as values, with the values corresponding to how many times the
# two keys appear in the same sentence.
# For example, if the semantic descriptor were
# sd = {...."fly":{"chicken": 2,..... "bird": 3}.....}
# then "fly" would have appeared in the same sentence as "bird" 3 times. 

# To build a semantic descriptor, one would need a text file sufficiently
# long such that it has enough data to work with. 

# There is a score that represents the correlation
# between two words, and that can be computed from many different formulas. 
# This includes the cosine similarity and the Euclidean space formula.

import math

def norm(vec):
    sum_of_squares = 0.0  
    for x in vec:
        sum_of_squares += vec[x] * vec[x]
    return math.sqrt(sum_of_squares)


def cosine_similarity(vec1, vec2):
    # a function used to calculate the correlation of two words
    
    top = 0
    bottom1, bottom2 = 0, 0
    for word in vec1:
        if word in vec2:
            top += vec1[word]*vec2[word]
    for word in vec1:
        bottom1 += (vec1[word])**2
    for word in vec2:
        bottom2 += (vec2[word])**2
    return top/math.sqrt(bottom1*bottom2)
            


def build_semantic_descriptors(sentences):
    # given a list of sentences, build a semantic descriptor
      
    semantic_descriptor = {}
    
    for item in sentences:
        L = list(set(item))
        if len(L) > 1:
            for word in L:
                if word != "":
                    word = word.lower()
                    if word in semantic_descriptor:
                        for this in L:
                            if this != word:
                                if this in semantic_descriptor[word]:
                                    semantic_descriptor[word][this] += 1
                                else:
                                    semantic_descriptor[word][this] = 1
                    else:
                        dic = {}
                        for this in L:
                            if this != word:
                                if this in dic:
                                    dic[this] += 1
                                else:
                                    dic[this] = 1
                            semantic_descriptor[word] = dic
        
    return semantic_descriptor

def build_semantic_descriptors_from_files(filenames):
    # given a list of filenames, make a semantic descriptor
    
    sentences = []
    for file in filenames:
        list = []
        f = open(file, "r", encoding="utf-8")
        f = f.read()
        f = f.lower()
        f = f.replace(",", " ")
        f = f.replace("-", " ")
        f = f.replace("--", " ")
        f = f.replace(":", " ")
        f = f.replace(";", " ")
        f = f.replace('"', " ")
        f = f.replace("'", " ")
        f = f.replace("?", ".")
        f = f.replace("\ufeff", " ")
        f = f.replace("!", ".")
        f_split = f.split(".")
        for item in f_split:
           list.append(item.split())
        sentences += list
    return build_semantic_descriptors(sentences)
       
           
def build_semantic_descriptors_from_files_percentage(filenames, percentage):
    # given a list of filenames and a percentage, build a semantic descriptor
    # corresponing to the first given percentage of the text. 
    
    sentences = []
    for file in filenames:
        list = []
        f = open(file, "r", encoding="utf-8")
        f = f.read()
        f = f.lower()
        f = f.replace(",", " ")
        f = f.replace("-", " ")
        f = f.replace("--", " ")
        f = f.replace(":", " ")
        f = f.replace(";", " ")
        f = f.replace('"', " ")
        f = f.replace("'", " ")
        f = f.replace("?", ".")
        f = f.replace("\ufeff", " ")
        f = f.replace("!", ".")
        f_split = f.split(".")
        for item in f_split:
           list.append(item.split())
        sentences += list[:int(percentage*len(list)/100)]
    return build_semantic_descriptors(sentences)
       
def most_similar_word(word, choices, semantic_descriptors, similarity_fn):
    # given a word, a list of words to test, a semantic descriptor, and a similarity function,
    # return the word from the list of words that is most similar to the first argument.

    output = choices[0]
    max = 0
    word = word.lower()
    for i in range (len(choices)):
        choices[i] = choices[i].lower()
    if word not in semantic_descriptors:
        return output
    for a in range (len(choices)):
        
        if choices[a] not in semantic_descriptors: 
            similarity = -1
        else:
            
            similarity = similarity_fn(semantic_descriptors[word], semantic_descriptors[choices[a]])
        if a == 0:
            max = similarity
        if similarity > max:
            max = similarity
            output = choices[a]
    return output


def run_similarity_test(filename, semantic_descriptors, similarity_fn):
    # this function uses an external file to run a simlarity test.
    # the file should have 4 words on each line.
    # for each line, we wish to find a word (given the choices of 
    # the third or the fourth) most smilar to the first, and the 
    # correct answer would be the second. This function runs the test
    # using a given similarity function, then calculates how many 
    # percent of the answers were right. 
    
    correct = 0.0
    f = open(filename, "r", encoding="utf-8")
    f = f.read()
    f = f.lower()
    f = f.strip("\ufeff")
    f = f.split("\n")
    list = []
    for item in f:
        if item != "":
            
           list.append(item.split())
    for set in list:
        if most_similar_word(set[0], set[2:], semantic_descriptors, similarity_fn) == set[1]:
            correct += 1
        
    return correct/len(list)*100
    
    
def euc_space(v1, v2):
    # utilizes the Euclidean space formula to calculate similarity 
    # this is a similarity function
    similarity = 0.0
    for key in v1:
        if key in v2:
            similarity += (v2[key] - v1[key])**2
        else:
            similarity += (v1[key])**2
    for key in v2:
        if v2[key] not in v1:
            similarity += (v2[key])**2
    return -1*math.sqrt(similarity)
    
            
def normalized_euc_space(v1, v2):
    # a similarity function implemented using the normalized
    # Euclidean space formula. 
    nv1 = norm(v1)
    nv2 = norm(v2)
    similarity = 0.0
    for key in v1:
        if key in v2:
            similarity += (v2[key]/nv2 - v1[key]/nv1)**2
        else:
            similarity += (v1[key]/nv1)**2
    for key in v2:
        if v2[key] not in v1:
            similarity += (v2[key]/nv2)**2
    return -1*math.sqrt(similarity)
    
    
if __name__ == '__main__':
    # insert functions here to try out the semantic descriptors.
    # Note that filenames should contain the full name (including directory).
    # example: sd = build_semantic_descriptors_from_files_percentage(["C:/Users/Ted Huang/Desktop/Git/Python/semantic_descriptors/Swann's Way.txt"], 10)