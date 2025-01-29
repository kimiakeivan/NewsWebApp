from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from .models import News

@registry.register_document
class NewsDocument(Document):
    class Index:
        name = "news"
        mapping = {
            "mappings": {
                "properties": {
                    "title": {
                        "type": "text",
                        "analyzer": "custom_english_analyzer"
                    },
                    "description": {
                        "type": "text",
                        "analyzer": "custom_english_analyzer"
                    },
                    "news_url": {
                        "type":"keyword"
                    }
                }
            },
        }
        setting = {
            "number_of_shards":1,
            "number_of_replicas":0,
            "analysis": {
                "analyzer": {
                    "custom_english_analyzer": {
                    "filter": [
                        "lowercase",
                        "stop",
                        "stemmer"
                    ],
                    "type": "custom",
                    "tokenizer": "standard"
                    }
                }
            }
        }

    class Django:
        model = News
        fields = {"name", "title", "description", "content", "category", "country", "view_count", "news_url", "image_url", "id"}
