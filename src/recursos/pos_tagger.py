from nltk.tag import StanfordPOSTagger
from nltk import word_tokenize, pos_tag
import os

PATH = os.getenv('STANFORD_POS_TAGGER')
JAR_PATH = PATH + '/stanford-postagger.jar'
MODEL_PATH = PATH + '/models/english-bidirectional-distsim.tagger'

def obtener_pos_tagger():
    pos_tagger_name = os.getenv('POS_TAGGER')
    if pos_tagger_name == 'STANFORD':
        return StanfordPOSTagger(MODEL_PATH, JAR_PATH, encoding='utf8').tag
    else:
        return pos_tag

tagger = obtener_pos_tagger()

def tag(texto):
    return tagger(word_tokenize(texto))
