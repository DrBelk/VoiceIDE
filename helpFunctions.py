import difflib
from constants import MIN_SOUND_DIFF

def list2str(list):
	return ",".join([str(e) for e in list])

def printlist(list):
	for i, e in enumerate(list):
		print (i, ':', e)
	
def str2(obj):
	return str(obj) if obj is not None else ""
	
def soundDiff(s1, s2):
	return difflib.SequenceMatcher(a = s1.lower(), b = s2.lower()).ratio() > MIN_SOUND_DIFF