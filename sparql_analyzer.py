import ld_utils
import httplib
import urllib
import json
from rdflib.term import URIRef, Literal
from sw_analyzer import SWAnalyzer

class SPARQLAnalyzer(SWAnalyzer):

    LIMIT = 100

    def __init__(self, sparql_endpoint):
        SWAnalyzer.__init__(self)
        self.sparql_endpoint = sparql_endpoint

    def open(self):
        SWAnalyzer.open(self)
        self.host, self.port, self.route = ld_utils.get_host_port_route(self.sparql_endpoint)
        self.sparql_http_connection = httplib.HTTPConnection(self.host, self.port)

    def load_graph(self):
        result = 0
        end = False
        it = 1
        offset = 0

        while not end:
            query = 'SELECT DISTINCT * WHERE { ?s ?p ?o } OFFSET %s LIMIT %s' % (str(offset), str(self.LIMIT))
            params = {'query': query, 'output': 'json'}
            headers = {'Accept': 'application/json'}
            self.sparql_http_connection.request('GET', self.route + '?' + urllib.urlencode(params), "", headers )
            response = self.sparql_http_connection.getresponse()
            if response.status == 200:
                data = response.read()
                json_data = json.loads(data)
                if len(json_data['results']['bindings']) > 0:
                    for json_triple in json_data['results']['bindings']:
                        subject = URIRef(json_triple['s']['value'])
                        predicate = URIRef(json_triple['p']['value'])
                        if json_triple['o']['type'] == "literal":
                            object = Literal(json_triple['o']['value'])
                        else:
                            object = URIRef(json_triple['o']['value'])
                        self.graph.add((subject, predicate, object))
                else:
                    end = True
            offset = (self.LIMIT * it)
            it = it + 1
            self.graph.commit()
        SWAnalyzer.load_graph(self)

    def close(self):
        SWAnalyzer.close(self)
        self.sparql_http_connection.close()
