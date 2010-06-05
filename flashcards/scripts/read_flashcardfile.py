#!/bin/python

from flashcards.models import *
import codecs

def read_flashcardfile(filename):
  #f = codecs.open(filename, 'r', 'utf-8')
  f = open(filename, 'r')
  for line in f.readlines():
    line = line.strip()
    if not line:
      continue
    words = line.split(':')
    wordA = words[0].strip()
    wordB = words[1].strip()
    if FlashCard.objects.filter(wordA=wordA).count():
      continue
    if FlashCard.objects.filter(wordB=wordB).count():
      continue
    FlashCard.add(wordA, wordB)
  f.close()
    
if __name__ == "__main__":
  from settings import FLASHCARD_FILENAME
  read_flashcardfile(FLASHCARD_FILENAME)
