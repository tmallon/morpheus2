import morpheuslib2
# Open our local cache.
cache = morpheuslib2.Cache.default()
print(cache.status)

# 2. Working with Latin text.


text = "urbem Romam a principio reges habuere" 


# Create a stream to process the words in this text.
ws = morpheuslib2.WordStream.from_text('Annals', text, 'la')

# Process the stream into a list of Word objects:
wx = ws.process()

# Make urls for each word:
urls = [w.make_url() for w in wx]

# The following call will try up to three times to fetch a response for these 
# urls. It returns a triple of results: tries is the number of tries made, resps
# the responses received, res indicates whether all were fetched successfully.
(tries, resps, res) = morpheuslib2.retry_all(urls, 3, cache)

print(str(tries) + ' tries made')
print('result ' + ('ok' if res else 'fetch problem - see message below'))

if res:
    # The next line make analysis lists out of the responses and words. 
    als = [resp.make_analysis_list(w) for (w,resp) in zip(wx, resps)]
    # Construct the filter for verbs:
    filter1 = [('pos', '=', 'verb')]
    # Loop through the analysis lists filtering for verbs:
    for i in range(0, len(als)):
        # 'verbs' is a list of Analysis objects.
        
        
        verbs = als[i].filter(filter1)
        for verb in verbs:
            print('[' + str(i) + ']:' + verb.get_feature('word') + ':'
                  + morpheuslib2.join(' ', *verb.inflections()) + ' of '
                  + verb.get_feature('lemma'))
            
            # Look for possible noun subjects, if the verb is 3rd person:
            # Use get_feature_nf() to deal with infinitives being classed as
            # verbs, but not having the person feature.
            
            if verb.get_feature_nf('person', 'none') == '3rd':
                num = verb.get_feature('number')
                # Construct the filter for nominative nouns with the same number:
                filter2 = [('pos', '=', 'noun'), ('case', '=', 'nom'), ('number', '=', num)]
                print("...Possible noun subjects:")
                for j in range(0, len(als)):
                    # Exclude noun analyses of the same word.
                    if j != i:
                        nouns = als[j].filter(filter2)
                        for noun in nouns:
                            print('...[' + str(j) + ']:' + noun.get_feature('word') + ':'
                            + morpheuslib2.join(' ', *noun.inflections()) + ' of '
                            + noun.get_feature('lemma'))                        
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