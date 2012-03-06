import os
import unittest
from grafatality import Grafatality

class BasicTest(unittest.TestCase):
    def delete_test_file(self, filename):
        f = open(filename, 'w')
        f.close()

    def cat(self, filename):
        f = open(filename)
        for line in f.readlines():
            print line
        f.close

    def setUp(self):
        self.test_filename = 'test.js'
        self.delete_test_file(self.test_filename)
        self.g = Grafatality(self.test_filename)

    def tearDown(self):
        self.delete_test_file('test.js')
        self.delete_test_file('other.js')

    def test_blow_up(self):
        """ it does not blow up on init """
        self.assertTrue(self.g.__class__)

    def test_adding_a_node(self):
        self.g.add_node('zach')
        self.assertTrue('zach' in self.g.graph.node)

    def test_adding_an_edge_with_explicit_node_creation(self):
        self.g.add_node('zach')
        self.g.add_node('waterloo')
        self.g.add_edge('zach', 'waterloo')
        self.assertTrue('waterloo' in self.g.graph['zach'])
        
    def test_adding_an_edge_with_implicit_node_creation(self):
        self.g.add_edge('zach', 'toronto')
        self.assertTrue('toronto' in self.g.graph['zach'])
        
    def test_adding_a_node_attribute(self):
        self.g.add_node('zach', political_leanings='libertarian')
        self.assertTrue(self.g.graph.node['zach']['political_leanings'] == 'libertarian')
        
    def test_adding_a_note_attribute_and_reading_it_correctly_in_another_graph(self):
        self.g.add_node('zach', political_leanings='libertarian')
        other = Grafatality('test.js')
        self.assertTrue(other.graph.node['zach']['political_leanings'] == 'libertarian')

    def test_adding_a_node_attribute_and_reading_it_correctly_in_another_graph_with_int(self):
        self.g.add_node('zach', age=26)
        other = Grafatality('test.js')
        self.assertTrue(other.graph.node['zach']['age'] == 26)
        
    def test_adding_an_edge_and_loading_it(self):
        self.g.add_edge('zach', 'toronto')
        other = Grafatality('test.js')
        self.assertTrue('toronto' in other.graph['zach'])
        
    def test_adding_an_edge_of_type_int_and_loading_it(self):
        self.g.add_edge('zach', 44)
        other = Grafatality('test.js')
        self.assertTrue(44 in other.graph['zach'])

    def test_adding_an_edge_attribute(self):
        self.g.add_edge('zach', 'toronto', key='stupid_key', lives_in=True)
        self.assertTrue(self.g.graph['zach']['toronto']['stupid_key']['lives_in'])
        
    def test_adding_an_edge_attribute_and_loading_it_again(self):
        self.g.add_edge('zach', 'toronto', key='stupid_key', lives_in=True)
        other = Grafatality('test.js')
        self.assertTrue(other.graph['zach']['toronto']['stupid_key']['lives_in'])
    
    def test_adding_an_edge_attribute_and_loading_it_again_with_int(self):
        self.g.add_edge('zach', 'toronto', key='stupid_key', time_of_res=3)
        other = Grafatality('test.js')
        self.assertTrue(other.graph['zach']['toronto']['stupid_key']['time_of_res'] == 3)
    
    def test_adding_an_edge_attribute_and_loading_it_again_with_float(self):
        self.g.add_edge('zach', 'toronto', key='stupid_key', time_of_res=3.5)
        other = Grafatality('test.js')
        self.assertTrue(other.graph['zach']['toronto']['stupid_key']['time_of_res'] == 3.5)
    
    def test_removal_of_an_edge(self):
        pass
    
    def test_removal_of_an_edge_and_loading_it_again(self):
        pass

    def test_removal_of_a_node(self):
        pass

    def test_removal_of_a_node_and_loading_it_again(self):
        pass

    def test_node_typing(self):
        self.g.add_node('zach', node_type='person')
        self.assertTrue('zach' in self.g.nodes_of_type('person', full=False))

    def test_retrival_of_nodes_of_a_certain_type(self):
        g = Grafatality('other.js')
        g.add_node('zach', node_type='person')
        self.assertTrue(('zach', 'person') in g.graph.node)
        self.assertTrue(('zach', 'person') in g.nodes_of_type('person'))

    def test_edge_typing(self):
        self.g.add_edge(('zach', 'person'), ('waterloo', 'university'), key='attended')
        self.assertTrue(('waterloo', 'university') in self.g.graph[('zach', 'person')])
        self.assertTrue('attended' in self.g.graph[('zach', 'person')][('waterloo', 'university')])
        
    def test_edge_typing_with_file_recall(self):
        self.g.add_edge(('zach', 'person'), ('waterloo', 'university'), key='attended')
        g = Grafatality('test.js')
        self.assertTrue(('waterloo', 'university') in g.graph[('zach', 'person')])
        self.assertTrue('attended' in g.graph[('zach', 'person')][('waterloo', 'university')])

    def test_edge_typing_with_attributes(self):
        self.g.add_edge(('ak47', 'gun'), ('russia','country'), key='origin', painful='yes')
        self.assertTrue(('russia', 'country') in self.g.graph[('ak47','gun')])
        self.assertTrue('origin' in self.g.graph[('ak47','gun')][('russia','country')])
        self.assertTrue('painful' in self.g.graph[('ak47','gun')][('russia','country')]['origin'])
        self.assertTrue('yes' == self.g.graph[('ak47','gun')][('russia','country')]['origin']['painful'])
        
        
    def test_edge_typing_with_attributes_and_file_recal(self):
        self.g.add_edge(('ak47', 'gun'), ('russia','country'), key='origin', painful='yes')
        g = Grafatality('test.js')
        self.assertTrue(('russia', 'country') in g.graph[('ak47','gun')])
        self.assertTrue('origin' in g.graph[('ak47','gun')][('russia','country')])
        self.assertTrue('painful' in g.graph[('ak47','gun')][('russia','country')]['origin'])
        self.assertTrue('yes' == g.graph[('ak47','gun')][('russia','country')]['origin']['painful'])
