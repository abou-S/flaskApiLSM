from flask import Flask, request, jsonify
from flask_cors import CORS
import spacy
import fr_core_news_md

nlp = fr_core_news_md.load()

app = Flask(__name__)

cors = CORS(app)

# suppression de Ponctuation et des determiant
def suppressionPonct(sentences):
  newSentence = []
  for index, word in enumerate(sentences):
    if word.tag_=='PUNCT' or word.tag_=='DET':
      if word.tag_=='DET' and 'Definite=Ind' or 'Definite=Def' in word.morph:
        pass
      elif word.tag_=='DET' :
        newSentence.append(word)
      pass
    elif word.tag_=='PRON':
      if word.dep_=='expl:comp':
        pass
      newSentence.append(word)
    elif word.tag_ == 'AUX':
      pass
    elif word.tag_ == 'ADP' and word.dep_ == 'case':
      pass
    else :
      newSentence.append(word)
  return newSentence
# Organisation de l'ordre des mots
def organizationOrdre(listWords):
  newSentences = []
  for word in listWords :
    if word.tag_=='VERB'and 'Tense=Past' in word.morph:
      sentenceProv = ['avant']
      newSentences.append(word.lemma_)
      sentenceProv.extend(newSentences)
      newSentences = sentenceProv
    elif 'Tense=Fut' in word.morph :
      sentenceProv = ['apres']
      newSentences.append(word.lemma_)
      sentenceProv.extend(newSentences)
      newSentences = sentenceProv
    elif word.lemma_ == 'je':
      newSentences.append('moi')
    elif word.lemma_ == 'tu' :
      newSentences.append('toi')
    elif word.lemma_ == 'il' :
      if 'Number=Plur' in word.morph :
        newSentences.append('eux')
      else :
        newSentences.append('lui')
    elif word.lemma_ == 'te':
        newSentences.append('toi')
    else:
      newSentences.append(word.lemma_)
  return newSentences


def list_a_renvoyer(text):
     words =[]



@app.route('/')
def hello_world():  # put application's code here
    return 'Hello World!'

@app.route('/traitement-texte', methods=['POST'])
def traitement_texte():
    data = request.json  # Attend un objet JSON avec une clé 'texte'
    texte = data.get('texte', '')
    list = words = []

    mots = texte
    doc = nlp(mots)
    listWords = suppressionPonct(doc)
    listOrdred = organizationOrdre(listWords)
    print(listOrdred)

    return jsonify({'mots': listOrdred})


if __name__ == '__main__':
    app.run()
