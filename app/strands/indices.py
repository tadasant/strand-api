from algoliasearch_django import AlgoliaIndex


class StrandIndex(AlgoliaIndex):
    fields = ('title', 'body', 'tag_names',)
    index_name = 'strands'
