from django.apps import AppConfig
import algoliasearch_django as algoliasearch

from app.strands.indices import StrandIndex


class StrandsAppConfig(AppConfig):
    name = 'app.strands'

    def ready(self):
        from app.strands.models import Strand  # Must import Strand model after the app is ready
        algoliasearch.register(Strand, StrandIndex)  # Registers the Strand model with algolia search
