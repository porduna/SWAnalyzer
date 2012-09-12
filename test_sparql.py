import unittest
from sparql_analyzer import SPARQLAnalyzer

class SPARQLAnalyzerTestCase(unittest.TestCase):

    def setUp(self):
        self.sparql_analyzer = SPARQLAnalyzer('http://www.morelab.deusto.es/joseki/articles')
        self.sparql_analyzer.open()
        self.sparql_analyzer.load_graph()

    def tearDown(self):
        self.sparql_analyzer.close()

    def test_get_classes(self):
        expected_classes = 13
        result_classes = len(self.sparql_analyzer.get_classes())
        self.assertEqual(result_classes, expected_classes)

    def test_get_properties(self):
        expected_properties = 79
        result_properties = len(self.sparql_analyzer.get_properties())
        self.assertEqual(result_properties, expected_properties)

    def test_get_subjects(self):
        expected_subjects = 241
        result_subjects = len(self.sparql_analyzer.get_subjects())
        self.assertEqual(result_subjects, expected_subjects)

    def test_get_objects(self):
        expected_objects = 1341
        result_objects = len(self.sparql_analyzer.get_objects())
        self.assertEqual(result_objects, expected_objects)

    def test_get_class_instances(self):
        expected_class_instances = 57
        result_class_instances = len(self.sparql_analyzer.get_class_instances('http://swrc.ontoware.org/ontology#Article'))
        self.assertEqual(result_class_instances, expected_class_instances)

    def test_get_property_count(self):
        expected_property_count = 478
        result_property_count = len(self.sparql_analyzer.get_property_count('http://xmlns.com/foaf/0.1/maker'))
        self.assertEqual(result_property_count, expected_property_count)

    def test_get_all_links(self):
        expected_links = 1877
        result_links = len(self.sparql_analyzer.get_all_links())
        self.assertEqual(result_links, expected_links)

class SPARQLAnalyzerInitialitation(unittest.TestCase):

    def setUp(self):
        self.sparql_analyzer = SPARQLAnalyzer('http://www.morelab.deusto.es/joseki/articles')
        self.sparql_analyzer.open()

    def tearDown(self):
        self.sparql_analyzer.close()

    def test_load_graph(self):
        expected_triples = 3843
        self.sparql_analyzer.load_graph()
        result_triples = len(self.sparql_analyzer.graph)
        self.assertEqual(result_triples, expected_triples)

if __name__ == '__main__':
    unittest.main()
