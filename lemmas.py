import morpheuslib2
# Open our local cache.
cache = morpheuslib2.Cache.default()
print(cache.status)

# 1. Finding lemmas of words.

# 1.A Latin.

# Making a Word instance is the first step:

w = morpheuslib2.Word.from_str('principatum', 'la')
url = w.make_url()

# Fetch the data, from the cache if possible:

resp = url.fetch(cache)

# Test the response:

if resp.is_ok():
    # Make an AnalysisList:
    al = resp.make_analysis_list(w)
    # Get the lemma feature of each analysis:
    lemmas = al.get_feature('lemma')
    print(lemmas)
    # A more informative print-out:
    print(al.word.word + " may be a :")
    for a in al:
        print(a.get_feature('pos') + ': '+ morpheuslib2.join(' ', *a.inflections()) + ' of ' + a.get_feature('lemma'))
    
else:
    # Print the problem:
    print(resp.exn)
    
# 1.B Repeat the process for Greek in Beta Code, but more succinctly:
w = morpheuslib2.Word.from_str('a)nti/on', 'greek', 'betacode')
resp = w.make_url().fetch(cache)
if resp.is_ok():
    al = resp.make_analysis_list(w)
    lemmas = al.get_feature('lemma')
    print(lemmas)
    print(al.word.word + " may be a :")
    for a in al:
        print(a.get_feature('pos') + ': '+ morpheuslib2.join(' ', *a.inflections()) + ' of ' + a.get_feature('lemma'))    
else:
    print(resp.exn)

# 1.C A Greek in Greek example.
w = morpheuslib2.Word.from_str('ἐγένετο', 'greek', 'greek')
resp = w.make_url().fetch(cache)
if resp.is_ok():
    al = resp.make_analysis_list(w)
    lemmas = al.get_feature('lemma')
    print(lemmas)
    print(al.word.word + " may be a :")
    for a in al:
        print(a.get_feature('pos') + ': '+ morpheuslib2.join(' ', *a.inflections()) + ' of ' + a.get_feature('lemma'))        
else:
    print(resp.exn)






# If the cache was changed by additions or removals, commit it. 

(will_be_deleted, _, will_be_added) = cache.commit_report()
if len(will_be_added) + len(will_be_deleted) > 0:
    print("committing memory cache")    
    cache.commit()
else:
    print("no commit of cache")