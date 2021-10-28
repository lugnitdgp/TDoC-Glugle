# import string
# from nltk.corpus import stopwords
# from nltk.tokenize import word_tokenize
# from nltk.stem.porter import PorterStemmer


# def clean(search_string): 
#     search_clean = search_string.lower()
#     translator = str.maketrans('', '', string.punctuation)
#     search_clean = search_clean.translate(translator)
#     stop_words = set(stopwords.words("english"))
#     search_clean = word_tokenize(search_clean)
#     print(search_clean)
#     search_clean = [word for word in search_clean if word not in stop_words]
#     stemmer = PorterStemmer()
#     print(search_clean)
#     search_clean = [stemmer.stem(word) for word in search_clean]
#     return search_clean


# query = "what is wikipedia in indians ??? "
# res = clean(query)
# res = ' '.join(str(e) for e in res)

# print(res)

# var = [{'_id': ObjectId('617160719cc79ed0f1a2f504') , 'url': 'https://meta.wikimedia.org/wiki/Special:MyLanguage/List_of_Wikipedias', 'title': 'List of Wikipedias - Meta', 'description': 'This page contains a list of all 323 languages for which official Wikipedias have been created under the auspices of the Wikimedia Foundation. The list includes 11 Wikipedias that were closed and moved to the Wikimedia Incubator for further development, leaving a current total of 312 active Wikipedias. Content in other languages is being developed at the Wikimedia Incubator; languages which meet certain criteria can get their own wikis.The table entries are ordered by current article count. Each entry gives the language name in English (linked to the English Wikipedia article for the language); its "local name" (i.e. in the language itself, linked to the article in that language\'s wiki); the language code used in the wiki\'s URL address and in interwiki links to it (linked to the local Main Page); and statistics on articles, edits, administrators, users, active users, and images (most linked to an appropriate local special page).To start a Wikipedia in a new language, please see our language proposal policy and the Incubator manual. Note: Just adding a link here does not create a new Wikipedia, nor does it serve to request that one be created.If a wiki becomes active and is not listed here, please post a notice on this article\'s talk page, including a link to all the relevant Wikipedia pages, and help promote the effort by announcing it on the Wikipedia-L mailing list, and at Wikimedia News.The tables here are regularly completely overwritten by a bot (using automatically gathered statistics from each wiki), so any edits made to individual entries won\'t last long, and are therefore usually unnecessary. If something is wrong with an entry other than simply having slightly outdated statistics, post about it on the talk page.More lists of Wikipedias by various criteria\u202f: \xa0[\u202fedit\u202f]The languages listed here are Wikipedias that have been created as separate subdomains of wikipedia.org, ordered by number of articles. The table includes closed Wikipedias whose domains still exist.Please visit the Wikimedia Incubator for new language versions (known as "tests") that may become stand-alone wikis in the future. See the Incubator Manual and FAQ for more information.These Wikipedias are closed and in read-only status. Existing users can still log in and their user preferences are still effective, but they cannot edit any pages. Editiable copies of these Wikipedias can be found in the Incubator; for example, the page cho:Chahta at the closed Choctaw Wikipedia can be found (and edited) at incubator:Wp/cho/Chahta.See also our Special:SiteMatrix, where the closed Wikipedias are crossed out (and the red links indicate wikis that have never existed). There is also a configuration file listing all closed Wikimedia projects.These Wikipedias are no longer hosted by Wikimedia. They have been moved to other hosts.These Wikipedias use language codes that do not conform to the ISO 639 standard (which is how wiki subdomains are chosen nowadays).Note that renaming wiki subdomains is very difficult, which is why so many of these nonstandard codes are still in use despite the existence of alternatives.'}]
# for dic in var:
#     for key , value in dic.items():
#         print(key , "valuse is " , value)
# print(var[1])

