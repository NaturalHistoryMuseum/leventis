from spacy.tokens import Span
from leventis.helpers import is_abbreviated_form


class AbbreviatedNames(object):

    name = "abbreviated_names"

    def __init__(self, nlp):
        Span.set_extension("taxon_name", default=None, force=True)
        Span.set_extension("taxon_is_abbreviated", default=False, force=True)

    def __call__(self, doc):
        for ent_index, ent in enumerate(doc.ents):
            if ent.label_ == "TAXON":
                # If this is abbreviated, rewind to a previous non-abbreviated taxon
                # To locate the family name
                if is_abbreviated_form(ent.string):
                    ent._.set("taxon_is_abbreviated", True)

                    # Loop back through previous entities, finding the first non-abbreviated
                    # form with same first letter
                    for i in range(ent_index - 1, -1, -1):
                        prev_ent = doc.ents[i]

                        if not is_abbreviated_form(prev_ent.string) and prev_ent.string[0] == ent.string[0]:
                            # Create a new taxonomic name with the parts from the two taxa
                            name_parts = [
                                prev_ent.string.split()[0],
                                ent.string.split()[1]
                            ]
                            ent._.set("taxon_name", ' '.join(name_parts))
                            break

                    # If we haven't found a non-abbreviated form, just use the full name
                    if not ent._.get("taxon_name"):
                        ent._.set("taxon_name", ent.string.strip())

                else:
                    ent._.set("taxon_name", ent.string.strip())

        return doc
