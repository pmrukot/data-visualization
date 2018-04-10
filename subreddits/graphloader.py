from pymongo import MongoClient

client = MongoClient()
db = client['reddit']

subs = db.subreddits.find()
nodes = [(sub['_id'],{'type': sub['type']}) for sub in subs]

relations = db.relations.find()
edges = [(r['sub_a'], r['sub_b']) for r in relations]

s_nodes = nodes[:10000]
s_edges = [edge for edge in edges if edge[0] in s_nodes and edge[1] in s_nodes]

