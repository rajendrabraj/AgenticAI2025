#
# !pip install nltk

corpus="""Hello Welcome,to Krish Naik's NLP Tutorials.Please do watch the entire course! to become expert in NLP.
"""

from nltk.tokenize import sent_tokenize
documents=sent_tokenize(corpus)
type(documents)
print(documents)


print("sentence tokenization   ")
print("=="*50   )

for sentence in documents:
    print(sentence)


## Tokenization 
## Paragraph-->words
## sentence--->words
from nltk.tokenize import word_tokenize
print("=="*50   )
print("Word  tokenization   ")

print("=="*50   )


word_tokenize(corpus)

for sentence in documents:
    print(word_tokenize(sentence))
    
from nltk.tokenize import wordpunct_tokenize
print("=="*50   )
print("Word  Punct tokenization   ")

print("=="*50   )

print(wordpunct_tokenize(corpus))
      


from nltk.tokenize import TreebankWordTokenizer
print("=="*50   )
print("Treebank Word tokenization   ")
print("=="*50   )


tokenizer=TreebankWordTokenizer()
print(tokenizer.tokenize(corpus))

print("=="*50   )        