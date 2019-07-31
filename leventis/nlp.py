
from pathlib import Path
import joblib
import spacy
from spacy.pipeline import EntityRuler

from leventis.components.entity_matcher import BiGramEntityMatcher
from leventis.components.sentenizer import Sentenizer
from leventis.components.expand_trait_entities import ExpandTraitEntities
from leventis.components.normalise_taxon_entities import NormaliseTaxonEntities
from leventis.components.abbreviated_names import AbbreviatedNames
from leventis.helpers import nlp_add_or_replace_pipe


class NLP(object):

    # Relative data path random
    data_path = Path(__file__).parent / 'data'

    model_path = data_path / 'models'

    def __init__(self, model_name):

        self.model = joblib.load(self.model_path / model_name)
        self.trait_patterns_file = self.data_path / 'trait_patterns.jsonl'
        self._nlp = self._build_nlp_pipeline()

    def _build_nlp_pipeline(self):

        nlp = spacy.load("en_core_sci_sm", disable=['ner'])

        nlp_add_or_replace_pipe(
            nlp, Sentenizer(), Sentenizer.name, before='parser'
        )

        nlp_add_or_replace_pipe(
            nlp, BiGramEntityMatcher(self.model), BiGramEntityMatcher.name
        )

        nlp_add_or_replace_pipe(
            nlp, NormaliseTaxonEntities(), NormaliseTaxonEntities.name, after=BiGramEntityMatcher.name
        )

        nlp_add_or_replace_pipe(
            nlp, AbbreviatedNames(nlp), AbbreviatedNames.name, after=NormaliseTaxonEntities.name
        )

        nlp_add_or_replace_pipe(
            nlp, EntityRuler(nlp).from_disk(self.trait_patterns_file), 'trait_ner', after=AbbreviatedNames.name
        )

        nlp_add_or_replace_pipe(
            nlp, ExpandTraitEntities(), ExpandTraitEntities.name, last=True
        )

        return nlp

    def __call__(self, text):
        return self._nlp(text)
