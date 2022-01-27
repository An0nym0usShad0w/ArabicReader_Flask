import sys
import string
import unicodedata

from camel_tools.morphology.database import MorphologyDB
from camel_tools.morphology.analyzer import Analyzer

from flask import Flask, render_template

arabic_str = """/[\u0600-\u06FF]/"""

db = MorphologyDB.builtin_db()

tbl = dict.fromkeys(i for i in range(sys.maxunicode)
                      if unicodedata.category(chr(i)).startswith('P'))

def remove_punctuation(text):
    return text.translate(tbl)

def analyse_word(word_):
    if word_ in string.punctuation:
        return
    if word_.isnumeric():
        return

    word = remove_punctuation(word_)

    analyzer = Analyzer(db)
    analyses = analyzer.analyze(word)

    if len(analyses) == 0:
        return

    if analyses[0]['pattern'] == 'FOREIGN':
        return

    filteredanalysis = []

    # add unique item to filtered-analysis array from Analyses
    filteredanalysis.append(analyses[0])
    for analysis in analyses:
        if analysis['stemgloss'] != filteredanalysis[-1]['stemgloss']:
            filteredanalysis.append(analysis)

    return filteredanalysis

def give_print_result(word):
    try:
        result = analyse_word(word)
    except:
        return "No results for: " + word
    final_result = word + '\n'
    counter = 0

    if result:
        for analysis in result:
            final_result += analysis['diac'] + '   ' + analysis['lex'] + '\n' + analysis['stemgloss'] + '  ' + \
                            analysis['stemcat'] + '  ' + analysis['gloss'] + '  ' + analysis['root'] + '\n\n'
            counter += 1
        final_result += 'No of results: ' + str(counter) + '\n'
        return final_result
    else:
        return "No results for: " + word

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/processUserInfo/<string:userInfo>', methods = ['POST'])
def processUserInfo(userInfo):
    print(userInfo)
    return give_print_result(userInfo)

if __name__ == '__main__':
    app.run(debug=True)
