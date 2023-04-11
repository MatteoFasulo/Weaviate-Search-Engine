import os
import weaviate

client = weaviate.Client(
    url = "http://localhost:8080",
)

schemaConfig = {
    'class': 'MyImages', # class name for schema config in Weaviate (change it with a custom name for your images)
    'vectorizer': 'img2vec-neural',
    'vectorIndexType': 'hnsw',
    'moduleConfig': {
        'img2vec-neural': {
            'imageFields': [
                'image'
            ]
        }
    },
    'properties': [
        {
            'name': 'image',
            'dataType': ['blob']
        },
        {
            'name': 'text',
            'dataType': ['string']
        }
    ]
}

try:
    client.schema.create_class(schemaConfig)
    print("Schema defined")
except Exception:
    print("Schema already defined, skipping...")