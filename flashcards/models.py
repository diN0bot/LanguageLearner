from django.db import models
import datetime

from lib import model_utils

class FlashCard(models.Model):
  wordA = models.CharField(max_length=200)
  wordB = models.CharField(max_length=200)
  
  added = models.DateTimeField(auto_now_add=True)
  
  number_right = models.IntegerField(default=0)
  number_wrong = models.IntegerField(default=0)
  answer_ratio = models.IntegerField(default=0)
  trouble_score = models.IntegerField(default=50)
  last_read = models.DateTimeField(auto_now=True)
    
  @classmethod
  def make(klass, wordA, wordB):
    return FlashCard(wordA=wordA,
                     wordB=wordB)
        
  def __unicode__(self):
    return "%s = %s (%s, %s)" % (self.wordA,
                                 self.wordB,
                                 self.number_right,
                                 self.number_wrong)

ALL_MODELS = [FlashCard]
