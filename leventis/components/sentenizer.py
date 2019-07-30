import re


# Custom sentenizer, which respects scientific names with var. and cf.


class Sentenizer(object):

    name = 'sentenizer'

    var_form_regex = re.compile('^var|cf$')

    def __call__(self, doc):
        previous_word = doc[0].text
        length = len(doc)
        for index, token in enumerate(doc):
            if (token.text == '.' and self.var_form_regex.match(previous_word) and index != (length - 1)):
                doc[index+1].sent_start = False
            previous_word = token.text
        return doc
