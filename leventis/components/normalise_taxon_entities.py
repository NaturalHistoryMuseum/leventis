from spacy.tokens import Span


class NormaliseTaxonEntities(object):

    name = "normalise_taxon_entities"

    tussenvoegsels = {'van', 'de', 'den',
                      'der', 'te', 'ten', 'ter', 'el', 'don'}
    et_al = {'et', 'al'}
    sect = {'sect', 'subsect'}
    subspecies = {'subsp', 'sp'}
    first_word_black_list = {'The', 'Its'}
    second_word_black_list = {'by', 'we', 'is', 'and', 'as', 'to', 'census'}

    def __call__(self, doc):
        ents = []
        for ent in doc.ents:
            if ent.label_ == "TAXON":
                word_parts = ent.string.split()

                if len(word_parts) < 2:
                    continue

                if self._is_blacklisted_first_word(word_parts[0]):
                    continue

                if self._is_blacklisted_second_word(word_parts[1]):
                    continue

                # I'm still getting some latin descriptive names marked
                # as taxon - even without the first letter capitalised - see 15995196
                if not self._is_capitalised_first_letter(word_parts[0]):
                    continue

                if self._second_word_is_single_letter(word_parts[1]):
                    continue

                # If this is a tussenvoegsel, continue to the next ent
                # skip adding it to the doc.ents
                if self._is_tussenvoegsel(word_parts[1]) or self._is_et_al(word_parts[1]):
                    continue

                if self._is_sect(word_parts[1]):
                    try:
                        first_sibling = doc[ent.start + 2]
                        second_sibling = doc[ent.start + 3]
                    except IndexError:
                        pass
                    else:
                        if not any([first_sibling.ent_type_, second_sibling.ent_type_]) and first_sibling.text == '.':
                            new_ent = Span(
                                doc, ent.start, ent.end + 2, label=ent.label)
                            ents.append(new_ent)
                        continue

                try:
                    first_sibling = doc[ent.start + 2]
                    second_sibling = doc[ent.start + 3]
                except IndexError:
                    pass
                else:

                    if not any([first_sibling.ent_type_, second_sibling.ent_type_]) and self._is_subspecies(first_sibling.string) and second_sibling.text == '.':
                        new_ent = Span(
                            doc, ent.start, ent.end + 3, label=ent.label
                        )
                        ents.append(new_ent)
                        continue

            ents.append(ent)

        doc.ents = ents
        return doc

    def _is_tussenvoegsel(self, word):
        return word in self.tussenvoegsels

    def _is_et_al(self, word):
        return word in self.et_al

    def _is_sect(self, word):
        return word in self.sect

    def _is_subspecies(self, word):
        return word in self.subspecies

    def _is_blacklisted_first_word(self, word):
        return word in self.first_word_black_list

    def _is_blacklisted_second_word(self, word):
        return word in self.second_word_black_list

    def _is_capitalised_first_letter(self, word):
        return word[0].isupper()

    def _second_word_is_single_letter(self, word):
        return len(word) <= 1
