import difflib
from constants import MIN_SOUND_DIFF

#from ru_soundex.distance import SoundexDistance
#from ru_soundex.soundex import RussianSoundex
#soundex = RussianSoundex(delete_first_letter=True)
#soundex_distance = SoundexDistance(soundex)

def list2str(list):
	return ",".join([str(e) for e in list])

def contextList2str(list):
	return "\n\n".join([str(e) for e in list])

def printlist(list):
	for i, e in enumerate(list):
		print (i, ':', e)
	
def str2(obj):
	return str(obj) if obj is not None else ""
	
def soundDiff(s1, s2):
    #return soundex_distance.distance(s1.lower(), s2.lower()) <= MIN_SOUND_DIFF
	return difflib.SequenceMatcher(a = s1.lower(), b = s2.lower()).ratio() > 0.8