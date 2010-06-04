import settings

from lib.view_utils import render_response, render_string, HttpResponseRedirect
from django.core.urlresolvers import reverse

from flashcards.models import *
from lib.view_utils import extract_parameters

def flashcard_by_id(request, id):
  flashcard = FlashCard.get_or_none(id=id)
  return render_flashcard(request, flashcard)

def flashcard_by_word(request, word):
  flashcard = FlashCard.get_or_none(languageA=word)
  if not flashcard:
    flashcard = FlashCard.get_or_none(languageB=word)
  return render_flashcard(request, flashcard)
  
def render_flashcard(request, flashcard):
  result = extract_parameters(request, "GET", [], [("both", False), ("B", False)])
  if not result['success']:
    return render_response(request, 'flashcards/error.html', {'error': result['reason']})
  print result
  both_sides = smart_bool(result['parameters']['both'])
  side_B = smart_bool(result['parameters']['B'])
  return render_response(request, 'flashcards/flashcard.html', locals())

def play(request):
  f = FlashCard.objects.all().order_by('?')
  if f.count() == 0:
    return render_response(request, 'flashcards/error.html', {'error': 'No flashcards'})
  
  return render_flashcard(request, f[0])


def right(request, id):
  flashcard = FlashCard.get_or_none(id=id)
  if flashcard:
    flashcard.number_right += 1
    flashcard.save()
  return HttpResponseRedirect(reverse('play'))

def wrong(request, id):
  flashcard = FlashCard.get_or_none(id=id)
  if flashcard:
    flashcard.number_wrong += 1
    flashcard.save()
  return HttpResponseRedirect(reverse('play'))

def smart_bool(s):
  """ parses a string into a boolean """
  if s is True or s is False:
    return s
  s = str(s).strip().lower()
  return not s in ['false','f','n','0','']
