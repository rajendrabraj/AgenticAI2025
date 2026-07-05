##Stemming
##Stemming is the process of reducing a word to its word stem that affixes to suffixes and prefixes or to the roots of words known as a lemma. Stemming is important in natural language ## understanding (NLU) and natural language processing (NLP).


## Classification Problem
## Comments of product is a positive review or negative review
## Reviews----> eating, eat,eaten [going,gone,goes]--->go

words=["eating","eats","eaten","writing","writes","programming","programs","history","finally","finalized"]

from nltk.stem import PorterStemmer

stemming=PorterStemmer()

print("=="*50   )
print("Porter Stemmer is a rule based stemmer which removes the common morphological and inflexional endings from words in English. It is one of the most popular stemming algorithms used in NLP tasks. The Porter Stemmer uses a set of rules to determine how to stem a word, and it can be customized to suit specific needs. The algorithm is designed to be efficient and effective, and it is widely used in applications such as information retrieval, text mining, and natural language processing.")
print("=="*50   )

for word in words:
    print(word+"---->"+stemming.stem(word))
    

print("=="*50   )
print("=="*50   )


stemming.stem('congratulations')

stemming.stem("sitting")

from nltk.stem import RegexpStemmer

print("=="*50   )

print("REG Ex Stemmer")
      
reg_stemmer=RegexpStemmer('ing$|s$|e$|able$', min=4)
print(reg_stemmer.stem('eating'))
print(reg_stemmer.stem('ingeating'))

print("=="*50   )




##Snowball Stemmer
## It is a stemming algorithm which is also known as the Porter2 stemming algorithm as it is a better version of the Porter Stemmer since some issues of it were fixed in this stemmer.

from nltk.stem import SnowballStemmer


snowballsstemmer=SnowballStemmer('english')


print("=="*50   )

print("Snowball Stemmer")
      

for word in words:
    print(word+"---->"+snowballsstemmer.stem(word))


print("=="*50   )


print(stemming.stem("fairly"),stemming.stem("sportingly"))
print("=="*50   )

print(snowballsstemmer.stem("fairly"),snowballsstemmer.stem("sportingly"))

print("=="*50   )

## Q&A,chatbots,text summarization
from nltk.stem import WordNetLemmatizer

lemmatizer=WordNetLemmatizer()


print("=="*50   )
print("Lemmatization is the process of reducing a word to its base or root form, known as a lemma. It is a more sophisticated approach than stemming, as it takes into account the context and meaning of the word. Lemmatization is important in natural language processing (NLP) and natural language understanding (NLU) tasks, as it helps to improve the accuracy of text analysis and information retrieval. The WordNetLemmatizer is a popular lemmatization algorithm that uses the WordNet lexical database to determine the lemma of a word based on its part of speech.")

print(lemmatizer)
print("=="*50   )

'''
POS- Noun-n , verb-v,adjective-a,adverb-r
'''
lemmatizer.lemmatize("going",pos='v')
# print(lemmatizer)
# print("=="*50   )
# lemmatizer.lemmatize("going",pos='n')
# print("=="*50   )
# lemmatizer.lemmatize("going",pos='a')
# print("=="*50   )
# lemmatizer.lemmatize("going",pos='r')
# print("=="*50   )


print("=="*50   )
words=["eating","eats","eaten","writing","writes","programming","programs","history","finally","finalized"]

print("=="*50   )

for word in words:
    print(word+"---->"+lemmatizer.lemmatize(word,pos='v'))
    print("=="*50   )
    print(word+"---->"+lemmatizer.lemmatize(word,pos='n'))
    print("=="*50   )
    print(word+"---->"+lemmatizer.lemmatize(word,pos='a'))
    print("=="*50   )
    print(word+"---->"+lemmatizer.lemmatize(word,pos='r'))

print("=="*50   )


print(lemmatizer.lemmatize("goes",pos='v'))

print("=="*50   )


print(lemmatizer.lemmatize("fairly",pos='v'),lemmatizer.lemmatize("sportingly"))
