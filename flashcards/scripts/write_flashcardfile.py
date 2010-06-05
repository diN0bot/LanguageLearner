#!/bin/python

from flashcards.models import *
from flashcards.scripts.read_flashcardfile import read_flashcardfile
from settings import FLASHCARD_FILENAME
import codecs

def write_flashcardfile(filename):
  f = codecs.open(filename, 'w', 'utf-8')
  for flashcard in FlashCard.objects.all():
    f.write('%s:%s\n' % (flashcard.wordA,
                         flashcard.wordB))
  f.close()
    
if __name__ == "__main__":
  #read_flashcardfile(FLASHCARD_FILENAME)
  write_flashcardfile(FLASHCARD_FILENAME)
