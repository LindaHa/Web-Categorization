import os.path
import pandas as pd
import nltk

file_input = 'Datasets/Dark_web_dataset - Copy (2).csv'
os.chdir("f:/Linda/Work work/Categorization")

output_file_relative = "Datasets/hopefully_categorized.csv"

char_blacklist = list(chr(i) for i in range(32, 127) if i <= 64 or i >= 91 and i <= 96 or i >= 123)
stopwords = nltk.corpus.stopwords.words('english')
stopwords.extend(char_blacklist)
english_vocab = set(w.lower() for w in nltk.corpus.words.words())
top = 250
toker = nltk.RegexpTokenizer(r'((?<=[^\w\s])\w(?=[^\w\s])|(\W))+', gaps=True)
stemmer = nltk.LancasterStemmer()

training_df = pd.read_csv(file_input)[['url', 'content', 'category']]
training_df_old = pd.read_csv(file_input)
training_df.append(training_df_old)
training_df['tokens_en'] = ''
training_df['confidence'] = ''

max_word_length = 100
def remove_non_english_documents(data_frame, english_tolerance = 20):
    print('remove_non_english_documents')
    english_confidence = []
    tokens_en = []
    for i, document in data_frame.iterrows():
        english_words = 0
        text = document['content']
        texts = text.split(' ')
        texts = [w for w in texts if len(w) < max_word_length]
        text = ' '.join(texts)

        wordies = nltk.word_tokenize(text)
        tokens = []
        for w in wordies:
            lower = w.lower()
            if lower in english_vocab:
                tokens.append(lower)
                english_words += 1
        tokens_en.append(tokens)
        english_confidence.append(english_words / len(wordies) * 100 if len(wordies) > 0 else 0)
    data_frame['english:confidence'] = english_confidence
    data_frame['tokens_en'] = tokens_en
    print('remove_non_english_documents end')
    return data_frame[data_frame['english:confidence'] > english_tolerance]


whole_df = remove_non_english_documents(training_df)
training_df = whole_df[whole_df['category'] != '']


def most_popular_words_per_category(data_frame, top_number=top):
    print('most_popular_words_per_category')
    words_of_category = {}
    for cat in set(data_frame['category'].values):
        all_words = []
        for wordies in data_frame[data_frame['category'] == cat]['tokens_en'].tolist():
            for w in wordies:
                all_words.append(w)
        all_word_except_stop_dist = nltk.FreqDist(
            stemmer.stem(w) for w in all_words if w not in stopwords and len(w) >= 3 and w[0] not in char_blacklist
        )

        most_common = all_word_except_stop_dist.most_common(top_number)
        words_of_category[cat] = [w for w, number in most_common]

    return words_of_category


words_frequency = most_popular_words_per_category(training_df)


def remove_clutter_words(words_per_category):
    print('remove_clutter_words')
    from flashtext.keyword import KeywordProcessor
    from collections import Counter
    wordies = []
    for cat in words_per_category.keys():
        wordies.extend(words_per_category[cat])
    words_counter = Counter(wordies)
    words_filter = {x: words_counter[x] for x in words_counter if words_counter[x] >= 7}
    words_stop = list(words_filter.keys())
    for cat in words_per_category.keys():
        words_per_category[cat] = [w for w in words_per_category[cat] if w not in words_stop]

    return words_per_category


words_frequency = remove_clutter_words(words_frequency)


from flashtext.keyword import KeywordProcessor
from collections import Counter


from flashtext.keyword import KeywordProcessor
from collections import Counter
all_keywords = []
word_processors = {}
print('word_processors')
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
def guess_category(text):
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

most_probable_categories = []
print('here')
for z, row in whole_df.iterrows():
    i = 0
    import pprint
    if i == 0:
        pprint.pprint(row)
        i += 1
    words = row['tokens_en']
    most_prob_cat = guess_category(words)
    most_probable_categories.append(most_prob_cat)
whole_df['category'] = most_probable_categories


whole_df.to_csv(output_file_relative, index=False)
