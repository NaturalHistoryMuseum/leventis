
class Tags(object):

    def __init__(self, tags):
        self._tags = tags

    def to_bilou(self):
        return self._convert_tags_to_biluo_tags(self._tags)

    def _convert_tags_to_biluo_tags(self, tags):
        tags_to_convert = set(tags)

        try:
            tags_to_convert.remove('O')
        except KeyError:
            pass

        biluo_tags = []

        for tag_to_convert in tags_to_convert:
            biluo_tags = self._convert_tag_to_bilou(tag_to_convert, tags)

        return biluo_tags

    def _convert_tag_to_bilou(self, tag_to_convert, tags):

        biluo_tags = []

        for i, tag in enumerate(tags):

            prev_tag = tags[i-1] if i else None
            next_tag = None if i+1 >= len(tags) else tags[i+1]

            if tag == tag_to_convert:

                # This will expand concurrently matched tags
                if prev_tag == tag_to_convert and next_tag == tag_to_convert:
                    bilou_tag = f'I-{tag_to_convert}'
                elif prev_tag == tag_to_convert:
                    bilou_tag = f'L-{tag_to_convert}'
                elif next_tag == tag_to_convert:
                    bilou_tag = f'B-{tag_to_convert}'

            else:
                bilou_tag = tag

            biluo_tags.append(bilou_tag)

        return biluo_tags


class BiGramTags(Tags):
    def to_bilou(self):
        unigram_tags = self._bigram_to_unigram(self._tags)
        return self._convert_tags_to_biluo_tags(unigram_tags)

    def _bigram_to_unigram(self, bigram_tags):

        unigram_tags = []
        for i, t in enumerate(bigram_tags):
            prev_tag = bigram_tags[i-1] if i > 0 else None
            tags = {t, prev_tag}

            tags.discard(None)

            if len(tags) > 1:
                tags.discard('O')

            unigram_tags.append(tags.pop())

        # The last tag is not a repeated bigram
        # So should always be included in the unigrams
        unigram_tags.append(bigram_tags[-1])
        return unigram_tags

    def _convert_tag_to_bilou(self, tag_to_convert, tags):

        biluo_tags = []

        for i, tag in enumerate(tags):

            next_tag = None if i+1 >= len(tags) else tags[i+1]
            prev_bilou_tag = biluo_tags[-1] if biluo_tags else None

            if tag == tag_to_convert:

                if prev_bilou_tag == f'B-{tag_to_convert}':
                    bilou_tag = f'L-{tag_to_convert}'
                elif next_tag == tag_to_convert:
                    bilou_tag = f'B-{tag_to_convert}'
                else:
                    bilou_tag = f'U-{tag_to_convert}'
            else:
                bilou_tag = tag

            biluo_tags.append(bilou_tag)

        return biluo_tags
