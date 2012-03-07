grafatality
===========

Essentially, it's a way of persisting a graph that you would normally hold in memory.

Building off of the networkx graph for inspiration, but it lacks node types as a built-in, which has limitations. I've stubbed in
typing with tuples (which are hashable) which persist to JSON arrays (which are not). Annoying, but really the only quirk so far.

Is it good?
----------

I love it for very quickly building prototypes, plus it makes apis very... easy.

Should I use it?
----------------

This should not be used on production systems. It is completely untested and likely to contain security bugs, etc.
If you want to play around with graphs, definitely. If you want to build a social network in an evening: definitely.

Is it fast?
-----------

Very.

But not as much as it could be. I was getting 500k node additions per second when I started, but 
data validation has slowed things down to 50k node additions per second. If this is the bottle neck in 
your toy webapp I question your use of the term 'toy webapp' if this is in your production system I 
question your sanity.

Usage
-----

Grafatality owns a networkx MultiDiGraph. I'm trying to keep the distinction 
since there are a lot of things you can already do with MultiDiGraphs in networkx
to access the graph directly (which you are expected to do) you do so through 
self.graph. There are method naming collisions between self and self.graph. That 
is intended. Only edges and nodes added through self are persisted. This is 
sometimes useful.

To add a node:

    self.g.add_node('zach')

To add a typed node:

    self.g.add_node('zach', node_type='person')

or:

    self.g.add_node(('zach', 'person'))

In order to keep things sane, a node is its identifier and its type, together in a 
tuple *is the node itself*. So ('zach', 'person') is the node. I know that is 
annoying but unless I want to recreate networkx from scratch that is what's 
happening. I'm sorry. On the bright side, as long as you are using 0.x.x of 
grafatality, this will not change. Though, there is no garuntee that 1.x.x will 
seperate the two.

To add an edge:

    self.g.add_edge('zach', 'waterloo')

Note that it automatically creates the nodes if not already on the graph.

To add an edge of typed nodes with an edge "type" (called "key" to be consistent 
with networkx) as well as edge attributes.

    self.g.add_edge(('ak47', 'gun'), ('russia','country'), key='origin', painful='yes')

To add a typed node with attributes.

    self.g.add_node('zach', age=26)

