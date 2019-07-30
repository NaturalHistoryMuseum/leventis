
import re


new_line_regex = re.compile(r'\n|\r')
extra_spaces_regex = re.compile(r'\s+')
variety_regex = re.compile(r'(\s)[v|y]a[v|r][,|.]\s?', re.IGNORECASE)
paragraph_hypenation_regex = re.compile(r'(\w)-[\s\n]+')


def text_preprocessor(text):
    text = normalise_variety(text)
    text = replace_paragraph_hyphenation(text)
    text = remove_new_lines(text)
    text = remove_extra_spaces(text)
    return text


def normalise_variety(text):
    # Correct common mispellings of variety (var.)
    # var, => var.
    # yar. => var.
    # yav, => var.
    return variety_regex.sub(r'\g<1>var. ', text)


def replace_paragraph_hyphenation(text):
    return paragraph_hypenation_regex.sub(r'\g<1>', text)


def remove_new_lines(text):
    return new_line_regex.sub(' ', text)


def remove_extra_spaces(text):
    return extra_spaces_regex.sub(' ', text)
