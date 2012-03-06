import os
import unittest
from grafatality import Grafatality

class BasicTest(unittest.TestCase):
    def setUp(self):
        def delete_test_file():
            f = open('test.js', 'w')
            f.close()
        delete_test_file()
        self.test_file = 'test.js'
        self.g = Grafatality(self.test_file)

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
    
    
