from sentence_transformers import SentenceTransformer
from pinecone import Pinecone, ServerlessSpec
import json,os
import uuid
from dotenv import load_dotenv
load_dotenv()

model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')


pc = Pinecone(api_key=os.getenv("PINECONE_API"))

index_name = 'sql-retrieval'

if index_name not in pc.list_indexes().names():
    pc.create_index(
        name=index_name,
        dimension=384,  
        metric='cosine',
        spec=ServerlessSpec(
            cloud='aws',      
            region='us-east-1'  
        )
    )

index = pc.Index(index_name)

print("index created..")
with open('nl_sql_pairs.json') as f:
    examples = json.load(f)

for ex in examples:
    embedding = model.encode(ex['nl']).tolist()
    index.upsert([(str(uuid.uuid4()), embedding, {'nl': ex['nl'], 'sql': ex['sql']})])

print("examples have been inserted..")