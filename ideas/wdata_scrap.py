import rdflib

graph = rdflib.Graph()
graph.parse(location='wkdata.ttl', format='n3')

results = graph.query(
    """
    PREFIX wd: <http://www.wikidata.org/entity/>
    PREFIX wdt: <http://www.wikidata.org/prop/direct/>
    PREFIX wikibase: <http://wikiba.se/ontology#>
    PREFIX p: <http://www.wikidata.org/prop/>
    PREFIX ps: <http://www.wikidata.org/prop/statement/>
    PREFIX pq: <http://www.wikidata.org/prop/qualifier/>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX bd: <http://www.bigdata.com/rdf#>

    SELECT ?itemLabel ?positionLabel WHERE {
      ?item wdt:P31 wd:Q5.
      ?item p:P106 ?position.
      SERVICE wikibase:label { bd:serviceParam wikibase:language "en". }
    }
    LIMIT 10
    """
)

for row in results:
    print(row.itemLabel, row.positionLabel)