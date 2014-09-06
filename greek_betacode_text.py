import morpheuslib2
# Open our local cache.
cache = morpheuslib2.Cache.default()
print(cache.status)

# Note the r prefix to the string literal. This causes backslashes not to be treated as escapes.
text = r"to\n d' au)= *thle/maxos pepnume/nos a)nti/on hu)/da:‘*)atrei+/dh, mh\ dh/ me polu\n xro/non e)nqa/d' e)/ruke.‘"



label = 'Odyssey'



ws = morpheuslib2.WordStream.from_text(label, text, 'greek', 'betacode')
wx = ws.process()
urls = [w.make_url() for w in wx]
(tries, resps, res) = morpheuslib2.retry_all(urls, 3, cache)
(tries, resps, res) = morpheuslib2.retry_all(urls, 3, cache)

print(str(tries) + ' tries made')
print('result ' + ('ok' if res else 'fetch problem - see message below'))
if res:
    # The next line make analysis lists out of the responses and words. 
    als = [resp.make_analysis_list(w) for (w,resp) in zip(wx, resps)]
    # Because of encoding matters with Greek, it is useful to discard 
    # returned analyses that do not match the word submitted.  
    [al.fix('form').discard_unmatched() for al in als]
    # Make a filter for nouns:
    filter1 = [('pos', '=', 'noun')]
    # Loop through the analysis lists filtering for nouns:
    for i in range(0, len(als)):
        
                
        # 'nouns' is a list of Analysis objects.        
        nouns = als[i].filter(filter1)    
        for noun in nouns:
            print('[' + str(i) + ']:' + noun.get_feature('word') + ':'
                  + morpheuslib2.join(' ', *noun.inflections()) + ' of '
                  + noun.get_feature('lemma'))      
            # Construct the filter for adjectives with case, gender and number agreement:
            filter2 = [('pos', 'in', ['adj', 'part']), 
                       ('case', '=', noun.get_feature('case')), 
                       ('number', '=', noun.get_feature('number')), 
                       ('gender', '=', noun.get_feature('gender'))]
            print("...Possible agreeing adjectives:")
            for j in range(0, len(als)):
                if j != i:
                    adjs = als[j].filter(filter2)
                    for adj in adjs:
                        print('...[' + str(j) + ']:' + adj.get_feature('word') + ':'
                        + morpheuslib2.join(' ', *adj.inflections()) + ' of '
                        + adj.get_feature('lemma'))                    
                    
else:
    # Print the failed responses:
        print("Failed responses:")
        for resp in resps:
            if not resp.is_ok():
                print(resp.exn)
                
# If the cache was changed by additions or removals, commit it. 

(will_be_deleted, _, will_be_added) = cache.commit_report()
if len(will_be_added) + len(will_be_deleted) > 0:
    print("committing memory cache")    
    cache.commit()
else:
    print("no commit of cache")    
    
  