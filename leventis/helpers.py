
import re


re_number = re.compile(r'\d+')

re_abbreviated_form = re.compile(r'\b[A-Z]\.')


# def abbreviate_scientific_name(scientific_name):
#     # FIX THIS
#     name_parts = scientific_name.split()
#     if len(name_parts) > 1:
#         return '{}. {}'.format(
#             name_parts[0][:1],
#             ' '.join(name_parts[1:])
#         )


def scientific_name_contains_number(scientific_name):
    return bool(re_number.search(scientific_name))


def is_abbreviated_form(word):
    return bool(re_abbreviated_form.search(word))


def nlp_add_or_replace_pipe(nlp, pipe, name, **kwargs):
    if name in nlp.pipe_names:
        nlp.replace_pipe(name, pipe)
    else:
        nlp.add_pipe(pipe, name, **kwargs)
