from flashtext.keyword import KeywordProcessor
from collections import Counter
all_keywords = []
word_processors = {}
for category in words_frequency.keys():
    all_keywords.extend(words_frequency[category])
    word_processor = KeywordProcessor()
    for word in words_frequency[category]:
        word_processor.add_keyword(word)
    word_processors[category] = word_processor
# remove duplicates
all_keywords = set(all_keywords)
all_keywords = list(all_keywords)
all_words_processor = KeywordProcessor()
for word in all_keywords:
    all_words_processor.add_keyword(word)



def compute_percentage(dum0, dumx):
    try:
        ans = float(dumx)/float(dum0)
        ans = ans * 100
    except:
        return 0
    else:
        return ans


## Create a function to find the most probable category
def guess_category(text, index):
    x=str(text)
    total_matches = len(all_words_processor.extract_keywords(x))
    if total_matches == 0:
        return 'Not working'

    matched_keywords_count = {}
    for p_key in word_processors:
        processor = word_processors[p_key]
        matched_keywords_count[p_key] = len(processor.extract_keywords(x))

    match_per_category = {}
    for tk_key in matched_keywords_count:
        matched = matched_keywords_count[tk_key]
        match_per_category[tk_key] = float(compute_percentage(total_matches, matched))

    max_prob_category = max(match_per_category, key=(lambda key: match_per_category[key]))
    return max_prob_category