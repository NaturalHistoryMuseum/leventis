from leventis.bhl.page import BHLPage
from leventis.nlp import NLP


class ParsePage(object):

    nlp = NLP('bi-gram-bernoulli-naive-bayes-model.pkl')

    def __init__(self, page_id):

        self._data = {}
        bhl_page = BHLPage(page_id)
        self.doc = self.nlp(bhl_page.get_normalised_text())
        self._parse_page()

    @property
    def taxa(self):
        return set(self._data.keys())

    @property
    def traits(self):
        return {k: v for k, v in self._data.items() if v}

    def _parse_page(self):

        taxon_subject = None

        for sent in self.doc.sents:

            taxa_ents = set(
                [ent for ent in sent.ents if ent.label_ == 'TAXON'])

            trait_ents = {
                ent.string for ent in sent.ents if ent.label_ == 'TRAIT'}

            if taxa_ents:

                [self._data.setdefault(taxa_ent._.taxon_name, set())
                 for taxa_ent in taxa_ents]

                if len(taxa_ents) == 1:
                    taxon_subject = taxa_ents.pop()
                else:
                    # TODO: Could add traits in if they immediately precede/succede e.g. 15989542
                    taxon_subject = None

            if taxon_subject and trait_ents:

                if trait_ents:
                    self._data[taxon_subject._.taxon_name] |= trait_ents
