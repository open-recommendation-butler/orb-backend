from collections import Counter
import spacy
import sqlite3

nlp = spacy.load('de_core_news_sm', disable=['textcat'])

def get_rubrik(text):

	indicators = {1: 'Politik', 2: 'Panorama', 3: 'Sport', 4: 'Wirtschaft', 5: 'Kultur', 6: 'Technik', 7: 'Reise', 8: 'Auto', 9: 'Gesundheit', 10: 'Wissen'}

	# Connect to Database
	conn = sqlite3.connect('article/helpers/get_rubrik_database.db')
	c = conn.cursor()

	# Process text with spaCy
	doc = nlp(text)

	# Crate a list of lowered words (exclude stop words, punctuation, brackets and urls)
	word_list = []

	for token in doc:
		if not token.is_stop and not token.is_punct and not token.is_space and not token.is_bracket and not token.like_url:	
			lemma = str(token.lemma_).lower()
			word_list.append(lemma)

	if len(word_list) == 0:
		return None

	# Count occcurences of words
	counted = Counter(word_list)


	word_dict = {}
	for key, value in counted.items():
		if str(value) in word_dict:
			word_dict[str(value)].append(key)
		else:
			word_dict[str(value)] = [key]


	columns = []
	for i in range(1,11):
		columns.append("`%s`" % str(i))


	sum_columns = []
	for i in range(1,11):
		sum_columns.append("SUM(`%s`)" % str(i))

	sum_columns = ", ".join(sum_columns)

	union_sel = []
	values = []
	for key, value in word_dict.items():
		columns_mul = [column + " * " + key + " AS " + column for column in columns]
		union_sel.append("SELECT " + ", ".join(columns_mul) + " FROM rubrik_words WHERE lemma IN (" + ", ".join(["?" for x in value]) + ")")
		values.extend(value)

	execute_str = "SELECT " + sum_columns + "FROM (" + " UNION ".join(union_sel) + ") AS sub;"

	c.execute(execute_str, values)

	werte = c.fetchone()
	results = []
	for i, wert in enumerate(werte):
		i +=  1
		results.append([i, wert])

	conn.close()

	try:
		results.sort(key=lambda x: x[1], reverse=True)
	except TypeError: # Prevent "TypeError: '<' not supported between instances of 'NoneType' and 'NoneType'"
		return None

	if results[0][1] - results[1][1] > 3:
		return indicators[results[0][0]]
	
	return None