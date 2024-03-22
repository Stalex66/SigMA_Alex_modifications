#%%

#%%
import networkx as nx
import random
import threading
import time

class GraphCreator():
    def __init__(self):
        pass
    def create_easyGraph(self):
        G = nx.Graph()
        G.add_nodes_from(['A1', 'A2', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3', 'C4'])
        G.add_edges_from([
            ('A1', 'B1'), ('A1', 'B2'), ('A1', 'C1'), ('A1', 'C2'), ('A1', 'C3'), ('B1', 'C1'),
            ('B2', 'C2'), ('B2', 'C3'),
            ('A2', 'C4'), ('A2', 'B3'), ('B3', 'C4')
        ])

        # Add random weights to all edges
        for u, v in G.edges():
            G[u][v]['weight'] = round(random.uniform(0.1, 1.0), 3)
    
        return G

    def create_advanced_graph(self):
        G = nx.Graph()
        G.add_nodes_from(['A1', 'A2', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3', 'C4', 'D1', 'D2', 'D3', 'D4', 'D5', 'E1', 'E2', 'E3', 'E4', 'E5'])
        G.add_edges_from([
            ('A1','B1'),('A1','B2'),('A1','C1'),('A1','C2'),('A1','C3'),('A1','D1'),('A1','D2'),('A1','D3'),('A1','D4'),('A1','E1'),('A1','E2'),('A1','E3'),('A1','E4'),
            ('A2','B3'),('A2','C4'),('A2','D5'),('A2','E5'),
            ('B1','C1'),('B1','D1'),('B1','E1'),
            ('B2','C2'),('B2','D2'),('B2','E2'),('B2','C3'),('B2','D3'),('B2','D4'),('B2','E3'),('B2','E4'),
            ('B3','C4'),('B3','D5'),('B3','E5'),
            ('C1','D1'),('C1','E1'),
            ('C2','D3'),('C2','D4'),('C2','E4'),('C2','E2'),
            ('C3','D2'),('C3','E2'),('C3','E3'),
            ('C4','D5'),('C4','E5'),
            ('D1','E1'),
            ('D2','E2'),('D2','E3'),
            ('D3','E2'),
            ('D4','E4'),
            ('D5','E5'),]
    
        )
        # Add random weights to all edges that simulate a pair of jaccardian similarity and jaccardian similiarity 
        for u, v in G.edges():
            G[u][v]['weight'] = round(random.uniform(0.1, 1.0), 3)
    
        return G

    def create_GraphX0(self):
        G = nx.Graph()
        G.add_nodes_from([1, 3, 4, 6, 10, 11])
        G.add_edges_from([
            (1, 3), (1, 4), (1, 6), (1, 10), (1, 11),
            (3, 6), (3, 10), (3, 11),
            (4, 10), (4, 11),
            (6, 10), (6, 11)
        ])
        # Add weights to all edges
        for u, v in G.edges():
            G[u][v]['weight'] = 0.5
        return G
    def create_random_graph(num_nodes, edge_probability):
        G = nx.Graph()
        nodes = list(range(1, num_nodes + 1))  # Nodes from 1 to num_nodes
        G.add_nodes_from(nodes)
        
        # Add random edges
        for i in range(len(nodes)):
            for j in range(i+1, len(nodes)):
                if random.random() < edge_probability:  # Edge probability as parameter
                    G.add_edge(nodes[i], nodes[j])
        
        # Add weights to all edges
        for u, v in G.edges():
            G[u][v]['weight'] = 0.5
        
        return G
    def create_random_graph_with_weights(num_nodes, edge_probability):
        G = nx.Graph()
        nodes = list(range(1, num_nodes + 1))  # Nodes from 1 to num_nodes
        G.add_nodes_from(nodes)
        
        # Add random edges
        for i in range(len(nodes)):
            for j in range(i+1, len(nodes)):
                if random.random() < edge_probability:  # Edge probability as parameter
                    G.add_edge(nodes[i], nodes[j])
        
        # Add weights to all edges
        for u, v in G.edges():
            G[u][v]['weight'] = round(random.uniform(0.1, 1.0), 3)
        
        return G

    def create_GraphX1(self):
        G = nx.Graph()
        G.add_nodes_from([1, 3, 4, 6, 10, 11])
        G.add_edges_from([
            (1, 3), (1, 4), (1, 6), (1, 10), (1, 11),
            (3, 6), (3, 10), (3, 11),
            (4, 10), (4, 11),
            (6, 10), (6, 11)
        ])
        # Add weights to all edges
        predefined_w = [1.0 / 3.0, 1.0 / 3.0, 2.0 / 3.0, 1.0 / 2.0, 1.0 / 2.0,
                        1.0 / 2.0, 1.0 / 4.0, 1.0 / 4.0, 1.0 / 4.0, 1.0 / 4.0,
                        2.0 / 5.0, 2.0 / 5.0]
        uv = 0
        for u, v in G.edges():
            G[u][v]['weight'] = predefined_w[uv]
            uv += 1
        return G

    def create_GraphX2(self):
        G = nx.Graph()
        G.add_nodes_from([1, 3, 4, 6, 10, 11])
        G.add_edges_from([
            (1, 3), (1, 4), (1, 6), (1, 10), (1, 11),
            (3, 6), (3, 10), (3, 11),
            (4, 10), (4, 11),
            (6, 10), (6, 11)
        ])
        # Add weights to all edges
        predefined_w = [1.0 / 3.0, 1.0 / 3.0, 1.0 / 3.0, 1.0 / 2.0, 1.0 / 2.0,
                        1.0 / 3.0, 1.0 / 4.0, 1.0 / 4.0, 1.0 / 4.0, 1.0 / 4.0,
                        1.0 / 4.0, 1.0 / 4.0]
        uv = 0
        for u, v in G.edges():
            G[u][v]['weight'] = predefined_w[uv]
            uv += 1
        return G
#%%
class NxGraphAssistant():
    def __init__(self):
        pass
    def is_complete_graph(G):
        """
        Check if a graph is complete.
    
        Parameters:
        - G: NetworkX graph
    
        Returns:
        - True if the graph is complete, False otherwise
        """
        for node in G:
            if len(G[node]) != len(G) - 1:
                return False
        return True
    
    def is_same_connections(graph, node1, node2):
        """
        Checks if two nodes have the same connections in a graph.
        
        Parameters:
        - graph: NetworkX graph
        - node1: node identifier
        - node2: node identifier
        
        Returns:
        - bool: True if nodes have the same connections, False otherwise
        """
        try:
            return (graph.neighbors(node1)) == set(graph.neighbors(node2))
        except:
            return False
    
    def all_connection_similar_but_to_each_other(graph, node1, node2):
        """
        Checks if two nodes have the same connections in a graph but are not connected to each other.
    
        Parameters:
        - graph: NetworkX graph
        - node1: node identifier
        - node2: node identifier
    
        Returns:
        - bool: True if nodes have the same connections but are not connected to each other, False otherwise
        """
        try:
            set1 = set(graph.neighbors(node1))
            set2 = set(graph.neighbors(node2))
    
            if node2 in set1:
                set1.remove(node2)
            if node1 in set2:
                set2.remove(node1)
    
            return set1 == set2
        except Exception as e:
            print(f"An error occurred: {e}")
            return False
    
    def connected(graph,node1, node2):
        """
        Checks if two nodes are connected in a graph.
    
        Parameters:
        - graph: NetworkX graph
        - node1: node identifier
        - node2: node identifier
    
        Returns:
        - bool: True if nodes are connected, False otherwise
        """
        try:
            return nx.has_path(graph, node1, node2)
        except:
            return False
    @staticmethod    
    def all_most_connected_nodes(entire_graph : nx.Graph ,sub_graph) :
        most_connected_nodes = [max(sub_graph, key=lambda x: len(entire_graph[x]))]
        for node in sub_graph:
            if len(entire_graph[node]) == len(entire_graph[most_connected_nodes[0]]) and node != most_connected_nodes[0]:
                most_connected_nodes.append(node)
                
        return most_connected_nodes
    @staticmethod
    def analyze_cliques(G,treshold=0.9):
        # Find cliques with Jaccardian similarity higher than 0.9

        cliques = [clique for clique in nx.find_cliques(G) if all(G.has_edge(u, v) and G[u][v]['weight'] > treshold for u, v in nx.utils.pairwise(clique))]


        # Calculate average Jaccardian value for each clique
        avg_jaccard_values = {}
        for clique in cliques:
            total_jaccard_value = sum(G[u][v]['weight'] for u, v in nx.utils.pairwise(clique))
            avg_jaccard_value = total_jaccard_value / len(clique)
            avg_jaccard_values[tuple(clique)] = avg_jaccard_value

        # Sort cliques by average Jaccardian value in descending order
        sorted_cliques = sorted(avg_jaccard_values.keys(), key=lambda x: avg_jaccard_values[x], reverse=True)
        print("Sorted Cliques:")
        print(sorted_cliques)
        print ("Avg Jaccard Values:")
        print(avg_jaccard_values)
        # Keep track of assigned nodes
        assigned_nodes = set()

        # remove all cliques that have nodes that are already assigned
        selected_cliques = []
        for clique in sorted_cliques:
            if not assigned_nodes.intersection(clique):
                selected_cliques.append(clique)
                assigned_nodes.update(clique)



        print("Selected Cliques:")
        print(selected_cliques)

        # create copy of graph G
        new_graph = G.copy()
        # iterate all cliques
        for clique in selected_cliques:
            # create a new node for the clique
            name = ""
            for node in clique:
                if name != "":
                    name += "+"
                name += str(node)
            new_node = name
            # add the new node to the new graph
            new_graph.add_node(new_node)
            # remove the old nodes from the new graph
            new_graph.remove_nodes_from(clique)
            # add edges between the new clique and the old nodes each clique member was connected to
            for node in clique:
                for neighbor in G.neighbors(node):
                    if neighbor not in clique and neighbor in new_graph.nodes():
                        new_graph.add_edge(new_node, neighbor)
                        print("Added edge between", new_node, "and", neighbor)
        return new_graph
    
    @staticmethod
    def plot_networkX_graph(G):
        import networkx as nx
        import matplotlib.pyplot as plt

        # Adjust the layout of the graph for better readability
        pos = nx.spring_layout(G, k=0.15)  # You can adjust the value of 'k' for desired spacing

        nx.draw(G, pos, with_labels=True, font_weight='bold')
        plt.show()

#%%

#%%
import networkx as nx
import uuid

class Custom_tree_node:
    def __init__(self, name):
        self.name = name
        self.uuid = uuid.uuid4()
        self.children = []
        self.parent = None 

    def add_child(self, child) -> 'Custom_tree_node':
        child.parent = self
        self.children.append(child)
        return child 

    def get_all_parts(self) -> list[str]:
        parts = []
        # split name by '+' and add each part to the list
        for part in self.name.split("+"):
            parts.append(part)
        return parts
    
    def get_len(self):
        return len(self.children)
    
    
class Counter:
    def __init__(self):
        self.count = 0
    def increment(self):
        self.count += 1
        return self.count



class Custom_Tree:

    def __init__(self):
        self.root = None
        self.graph = nx.Graph()

    def add_node(self, parent_uuid, child_name):
        if not self.root:
            self.root = Custom_tree_node(child_name)
            return self.root
        
        node_return = self.root
        parent_node = self._find_node(self.root, parent_uuid)
        if parent_node:
            node_return = parent_node.add_child(Custom_tree_node(child_name))
        else:
            print("Parent node not found.")
        # return new node
        return node_return           
    
    def get_size(self, node=None):
        if not node:
            node = self.root

        if not node.children:
            return 1

        size = 1
        for child in node.children:
            size += self.get_size(child)

        return size
    def get_depth(self, node=None, depth=0):
        if not node:
            node = self.root

        if not node.children:
            return depth

        max_depth = depth
        for child in node.children:
            child_depth = self.get_depth(child, depth + 1)
            max_depth = max(max_depth, child_depth)

        return max_depth
            
        

    def _find_node(self, node, target_uuid):
        if node.uuid == target_uuid:
            return node
        for child in node.children:
            found = self._find_node(child, target_uuid)
            if found:
                return found
        return None

    def print_tree(self, node=None, depth=0):
        if not node:
            node = self.root
        #print(f"{node.name}({node.uuid})")
        print(f"{node.name}")
        if node.children:
            for i, child in enumerate(node.children):
                if i < len(node.children) - 1:
                    print("  " * (depth + 1) + "├── ", end="")
                else:
                    print("  " * (depth + 1) + "└── ", end="")
                self.print_tree(child, depth + 2)

    def problem_handler_create_multiple_trees_on_conflict(self, G, current_graph, most_connected_nodes,last_node=None):
            '''
            In case of conflict it creates multiple subtrees for each most connected node and adds them to the tree
            '''
            for node in most_connected_nodes:
                print("iteration")
                most_connected_node = node
                edited_graph = G.subgraph(current_graph).copy()
                for node in most_connected_nodes:
                    if node != most_connected_node:
                        edited_graph.remove_node(node)
                for node in current_graph:
                    if not NxGraphAssistant.connected(edited_graph, most_connected_node, node):
                        try:
                            edited_graph.remove_node(node)
                        except:
                            continue
                print("added:", most_connected_node)
                print("to parent", last_node.name)
                for current_subgraph in nx.connected_components(edited_graph):
                    print("-last node", last_node.name)
                    print("-most connected node", most_connected_node)
                    print("-current subgraph", current_subgraph)
                    self.find_complete_subgraphs_in_connected_graph(G, current_subgraph,last_node)
               

                    
    def problem_handler_create_multiple_trees_on_conflict_advanced(self, G, current_graph, most_connected_nodes, last_node=None, depth=2, first=True):
        '''
        Puts further nodes in the tree if at least one complete subgraph is found
        '''
        # Sort most_connected_nodes for deterministic behavior
        most_connected_nodes = sorted(most_connected_nodes)
        correct_count = Counter()
        for node in most_connected_nodes:
            most_connected_node = node
            edited_graph = G.subgraph(current_graph).copy()
            for node in most_connected_nodes:
                if node != most_connected_node:
                    edited_graph.remove_node(node)
            for node in current_graph:
                if not NxGraphAssistant.connected(edited_graph, most_connected_node, node):
                    try:
                        edited_graph.remove_node(node)
                    except:
                        continue
            for current_subgraph in nx.connected_components(edited_graph):
                # check if most connected node is in the subgraph
                if most_connected_node in current_subgraph:
                    if NxGraphAssistant.is_complete_graph(G.subgraph(current_subgraph)) or len(current_subgraph) == 1:
                        correct_count.increment()
                    else:
                        if depth > 1:
                            # new most connected nodes
                            current_subgraph.remove(most_connected_node)
                            new_most_connected_nodes = NxGraphAssistant.all_most_connected_nodes(G, current_subgraph)
                            print("new most connected nodes", new_most_connected_nodes)
                            self.problem_handler_kill_tree_if_no_complete_subtree(G, current_subgraph, new_most_connected_nodes, last_node, depth - 1, False)

            if(correct_count.count > len(most_connected_nodes)/depth):
                for node in most_connected_nodes:
                    print("iteration")
                    most_connected_node = node
                    edited_graph = G.subgraph(current_graph).copy()
                    for node in most_connected_nodes:
                        if node != most_connected_node:
                            edited_graph.remove_node(node)
                    for node in current_graph:
                        if not NxGraphAssistant.connected(edited_graph, most_connected_node, node):
                            try:
                                edited_graph.remove_node(node)
                            except:
                                continue
                    print("added:", most_connected_node)
                    print("to parent", last_node.name)
                    for current_subgraph in nx.connected_components(edited_graph):
                        print("-last node", last_node.name)
                        print("-most connected node", most_connected_node)
                        print("-current subgraph", current_subgraph)
                        self.find_complete_subgraphs_in_connected_graph(G, current_subgraph,last_node)
                    
 
    def problem_handler_kill_tree_if_no_complete_subtree(self, G, current_graph, most_connected_nodes, last_node=None, depth=2, first=True):
        '''
        Puts further nodes in the tree if at least one complete subgraph is found
        '''
        # Sort most_connected_nodes for deterministic behavior
        #todo does notwork for str
        #most_connected_nodes = sorted(most_connected_nodes)
        
        for node in most_connected_nodes:
            print("iteration - kill")
            most_connected_node = node
            edited_graph = G.subgraph(current_graph).copy()
            for node in most_connected_nodes:
                if node != most_connected_node:
                    edited_graph.remove_node(node)
            for node in current_graph:
                if not NxGraphAssistant.connected(edited_graph, most_connected_node, node):
                    try:
                        edited_graph.remove_node(node)
                    except:
                        continue
            for current_subgraph in nx.connected_components(edited_graph):
                # check if most connected node is in the subgraph
                if most_connected_node in current_subgraph:
                    print("most connected node in subgraph", current_subgraph)
                    if NxGraphAssistant.is_complete_graph(G.subgraph(current_subgraph)) or len(current_subgraph) == 1:
                        if first:
                            name = ""
                            for node in current_subgraph:
                                if name != "":
                                    name += "+"
                                name += str(node)
                            last_node = self.add_node(last_node.uuid, name)
                            print("complete subgraph - success1", current_subgraph)
                            return

                        else:
                            print("return true")
                            return True
                    else:
                        print("not complete subgraph", current_subgraph)
                        if depth > 1:
                            # new most connected nodes
                            current_subgraph.remove(most_connected_node)
                            new_most_connected_nodes = NxGraphAssistant.all_most_connected_nodes(G, current_subgraph)
                            print("new most connected nodes", new_most_connected_nodes)
                            if self.problem_handler_kill_tree_if_no_complete_subtree(G, current_subgraph, new_most_connected_nodes, last_node, depth - 1, False):
                                if first:
                                    # add uppest node to the tree
                                    print("complete subgraph - success2", current_subgraph)
                                    print("most connected node", most_connected_node)
                                    last_node = self.add_node(last_node.uuid, most_connected_node)
                                    for subgraph in nx.connected_components(G.subgraph(current_subgraph)):
                                        #new_most_connected_nodes = NxGraphAssistant.all_most_connected_nodes(G, subgraph)
                                        #self.problem_handler_kill_tree_if_no_complete_subtree(G, subgraph, new_most_connected_nodes, last_node, depth - 1)
                                        self.find_complete_subgraphs_in_connected_graph(G, subgraph, last_node)

                                else:
                                    print("complete subgraph - give further", current_subgraph)
                                    return True
        return False
    
    # needs testing
    def problem_handler_kill_tree_if_no_complete_subtree_all(self, G, current_graph, most_connected_nodes, last_node=None, depth=2, first=True):
        '''
        only puts further nodes in the tree if all the subgraph is complete
        '''
        # Sort most_connected_nodes for deterministic behavior
        most_connected_nodes = sorted(most_connected_nodes)
        
        for node in most_connected_nodes:
            print("iteration - kill")
            most_connected_node = node
            edited_graph = G.subgraph(current_graph).copy()
            for node in most_connected_nodes:
                if node != most_connected_node:
                    edited_graph.remove_node(node)
            for node in current_graph:
                if not NxGraphAssistant.connected(edited_graph, most_connected_node, node):
                    try:
                        edited_graph.remove_node(node)
                    except:
                        continue
            for current_subgraph in nx.connected_components(edited_graph):
                # if contains most connected node
                if most_connected_node in current_subgraph:
                    if not NxGraphAssistant.is_complete_graph(G.subgraph(current_subgraph)) or len(current_subgraph) == 1:
                        return
            for current_subgraph in nx.connected_components(edited_graph):
                # add complete graph to tree
                if most_connected_node in current_subgraph:
                    name = ""
                    for node in current_subgraph:
                        if name != "":
                            name += "+"
                        name += str(node)
                    if last_node is None:
                        last_node = self.add_node(0,name)
                    else:
                        last_node = self.add_node(last_node.uuid,name)

    def find_complete_subgraphs_in_connected_graph_mt(self, G, current_graph, last_node=None, problem_solver=problem_handler_create_multiple_trees_on_conflict_advanced):
        graph = G
        if NxGraphAssistant.is_complete_graph(G.subgraph(current_graph)):
            name = ""
            for node in current_graph:
                if name != "":
                    name += "+"
                name += str(node)
            if last_node is None:
                last_node = self.add_node(0, name)
            else:
                last_node = self.add_node(last_node.uuid, name)
            print("complete graph", name)
        else:
            most_connected_nodes = NxGraphAssistant.all_most_connected_nodes(G, current_graph)
            # This is the "problematic case"
            if len(most_connected_nodes) > 1:
                if last_node is None:
                    last_node = self.add_node(0, "root")
                print("case more than one most connected node")
                print("most connected nodes", most_connected_nodes)
                # print type of problem solver
                print("problem solver", type(problem_solver))
                problem_solver(self, G=G, current_graph=current_graph, most_connected_nodes=most_connected_nodes,
                            last_node=last_node)
            else:
                print("case one most connected node")
                most_connected_node = most_connected_nodes[0]
                print("most connected node", most_connected_node)
                if last_node is None:
                    last_node = self.add_node(0, most_connected_node)
                else:
                    last_node = self.add_node(last_node.uuid, most_connected_node)
                edited_graph = G.subgraph(current_graph).copy()
                edited_graph.remove_node(most_connected_node)

                # Process subgraphs in separate threads
                threads = []
                for current_subgraph in nx.connected_components(edited_graph):
                    t = threading.Thread(target=self.find_complete_subgraphs_in_connected_graph,
                                        args=(G, current_subgraph, last_node))
                    threads.append(t)
                    t.start()

                # Wait for all threads to complete
                for t in threads:
                    t.join()
    def find_complete_subgraphs_in_connected_graph(self, G, current_graph, last_node=None, problem_solver = problem_handler_create_multiple_trees_on_conflict):
        graph = G
        if NxGraphAssistant.is_complete_graph(G.subgraph(current_graph)):
            name = ""
            for node in current_graph:
                if name != "":
                    name += "+"
                name += str(node)
            if last_node is None:
                last_node = self.add_node(0,name)
            else:
                last_node = self.add_node(last_node.uuid,name)
            
            print("complete graph", name)
        else:
            most_connected_node = []
            most_connected_nodes = NxGraphAssistant.all_most_connected_nodes(G, current_graph)
            # this ist the "problematic case"
            if len(most_connected_nodes) > 1:
                if last_node is None :
                    last_node = self.add_node(0,"root")
                print("case more than one most connected node")
                print("most connected nodes", most_connected_nodes)
                # print type of problem solver
                print("problem solver", type(problem_solver))
                problem_solver(self,G = G, current_graph = current_graph,most_connected_nodes = most_connected_nodes, last_node = last_node)
            else:
                print("case one most connected node")
                most_connected_node = most_connected_nodes[0]
                print("most connected node", most_connected_node)
                if last_node is None:
                    last_node = self.add_node(0,most_connected_node)
                else:
                    last_node = self.add_node(last_node.uuid,most_connected_node)
                edited_graph = G.subgraph(current_graph).copy()
                edited_graph.remove_node(most_connected_node)
                for current_subgraph in nx.connected_components(edited_graph):
                    self.find_complete_subgraphs_in_connected_graph(G, current_subgraph,last_node)




    def problem_handler_create_multiple_trees_on_conflict_advanced_mt(self, G, current_graph, most_connected_nodes, last_node=None, depth=3, first=True):
        '''
        Puts further nodes in the tree if at least one complete subgraph is found
        '''
        # Sort most_connected_nodes for deterministic behavior
        most_connected_nodes = sorted(most_connected_nodes)
        correct_count = Counter()

        # Create a lock for thread-safe access
        lock = threading.Lock()

        # Function to run in threads
        def process_node(node):
            nonlocal correct_count
            most_connected_node = node
            edited_graph = G.subgraph(current_graph).copy()
            for node in most_connected_nodes:
                if node != most_connected_node:
                    edited_graph.remove_node(node)
            for node in current_graph:
                if not NxGraphAssistant.connected(edited_graph, most_connected_node, node):
                    try:
                        edited_graph.remove_node(node)
                    except:
                        continue
            for current_subgraph in nx.connected_components(edited_graph):
                # check if most connected node is in the subgraph
                if most_connected_node in current_subgraph:
                    if NxGraphAssistant.is_complete_graph(G.subgraph(current_subgraph)) or len(current_subgraph) == 1:
                        with lock:
                            correct_count.increment()
                    else:
                        if depth > 1:
                            # new most connected nodes
                            current_subgraph.remove(most_connected_node)
                            new_most_connected_nodes = NxGraphAssistant.all_most_connected_nodes(G, current_subgraph)
                            print("new most connected nodes", new_most_connected_nodes)
                            self.problem_handler_kill_tree_if_no_complete_subtree(G, current_subgraph, new_most_connected_nodes, last_node, depth - 1, False)

        # Create and start threads
        threads = []
        for node in most_connected_nodes:
            t = threading.Thread(target=process_node, args=(node,))
            threads.append(t)
            t.start()

        # Wait for all threads to complete
        for t in threads:
            t.join()

        if (correct_count.count > len(most_connected_nodes) / depth):
            for node in most_connected_nodes:
                print("iteration")
                most_connected_node = node
                edited_graph = G.subgraph(current_graph).copy()
                for node in most_connected_nodes:
                    if node != most_connected_node:
                        edited_graph.remove_node(node)
                for node in current_graph:
                    if not NxGraphAssistant.connected(edited_graph, most_connected_node, node):
                        try:
                            edited_graph.remove_node(node)
                        except:
                            continue
                print("added:", most_connected_node)
                print("to parent", last_node.name)
                for current_subgraph in nx.connected_components(edited_graph):
                    print("-last node", last_node.name)
                    print("-most connected node", most_connected_node)
                    print("-current subgraph", current_subgraph)
                    self.find_complete_subgraphs_in_connected_graph(G, current_subgraph, last_node)
                    
#%%


class ClusteringHandler():
    def __init__(self):
            pass
    def do_all(self,G,solver):
        trees = []
        for g in nx.connected_components(G):
            tree = Custom_Tree()
            graph = G.subgraph(g)
            tree.find_complete_subgraphs_in_connected_graph(graph, g,None,solver)
            trees.append(tree)
        return trees
    def do_all_advanced(self,G,solver):
        trees = []
        for g in nx.connected_components(G):
            tree = Custom_Tree()
            graph = G.subgraph(g)
            tree.find_complete_subgraphs_in_connected_graph_mt(graph, g,None,solver)
            trees.append(tree)

        # Print all trees
        for tree in trees:
            tree.print_tree()
            print("---")
        return trees  

#%%
clusterMaster = ClusteringHandler()
graph = GraphCreator.create_random_graph_with_weights(70,0.2)
    
#%%

#graph = GraphCreator.create_random_graph_with_weights(num_nodes=40, edge_probability=0.3)

#graph = GraphCreator().create_advanced_graph()
#graph = GraphCreator().create_random_graph_with_weights(50, 0.5)
#graph = NxGraphAssistant.analyze_cliques(graph,0.2)
#NxGraphAssistant.plot_networkX_graph(graph)
# start time measurement
start_time1 = time.time()
#T1 = clusterMaster.do_all(graph,Custom_Tree.problem_handler_create_multiple_trees_on_conflict_advanced)
end_time1 = time.time()
start_time2 = time.time()
graph = NxGraphAssistant().analyze_cliques(graph,0.5)
T2 = clusterMaster.do_all(graph,Custom_Tree.problem_handler_create_multiple_trees_on_conflict_advanced)
end_time2 = time.time()
print("Time v1:" , end_time1 - start_time1)
print("Time v2:" , end_time2 - start_time2)
'''
for tree in T1:
    # print size and depth of tree
    print("Tree1")
    print("Size:", tree.get_size())
    print("Depth:", tree.get_depth())
    #tree.print_tree()
'''
for tree in T2:
    # print size and depth of tree
    print("Tree2")
    print("Size:", tree.get_size())
    print("Depth:", tree.get_depth())
    #tree.print_tree()

#%%

#%%
