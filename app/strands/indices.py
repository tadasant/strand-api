from algoliasearch_django import AlgoliaIndex


class StrandIndex(AlgoliaIndex):
    fields = ('title', 'body', 'tag_names',)  # Defines the fields in the Strand index (map to fields on Strand model)
    index_name = 'strands'  # Defines the name of the index. The config files define prefixes (e.g. dev_, prod_).
