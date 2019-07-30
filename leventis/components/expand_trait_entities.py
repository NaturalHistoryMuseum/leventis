from spacy.tokens import Span


class ExpandTraitEntities(object):

    name = "expand_trait_entities"

    def _get_token(self, doc, x):
        try:
            return doc[x]
        except IndexError:
            return None

    def _expand_start(self, doc, ent_start):
        # To get the preceding token, we need to get ent_start -1
        # Expansion is greedy to end - this ensures it does not expand
        # into previous new entities
        try:
            max_end = max([e.end for e in self.new_ents])
        except ValueError:
            pass
        else:
            if ent_start <= max_end:
                return ent_start

        if self._preceeding_token_is_expandable(doc, ent_start):
            ent_start = self._expand_start(doc, ent_start - 1)
        return ent_start

    def _expand_end(self, doc, ent_end):
        if self._succeeding_token_is_expandable(doc, ent_end):
            ent_end = self._expand_end(doc, ent_end + 1)
        return ent_end

    def __call__(self, doc):
        self.new_ents = []
        for ent in doc.ents:
            if ent.label_ == "TRAIT":
                ent_start = self._expand_start(doc, ent.start)
                ent_end = self._expand_end(doc, ent.end)
                new_ent = Span(doc, ent_start, ent_end, label=ent.label)
                self.new_ents.append(new_ent)
            else:
                self.new_ents.append(ent)

        doc.ents = self.new_ents

        return doc

    def _preceeding_token_is_expandable(self, doc, ent_start):
        return self._token_is_expandable(doc, ent_start - 1)

    def _succeeding_token_is_expandable(self, doc, ent_end):
        return self._token_is_expandable(doc, ent_end)

    def _token_is_expandable(self, doc, ent_end):
        token = self._get_token(doc, ent_end)
        if token:
            return (token.pos_ in ['NUM', 'SYM', 'ADV', 'ADJ'] or token.dep_ in ['quantmod'] or token.lower_ in ['mm', 'cm', 'inch', 'inches']) and not token.ent_type_

        # # @staticmethod
        # # def _token_is_entity(token):
        # #     return token.ent_type_

        # def _is_overlapping(self, token):
        #     print(token)
        #     return True
