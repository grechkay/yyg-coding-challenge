from collections import defaultdict

class AveCountGraph:
    """
    Data structure that maintains the following:
    1. Set of vertex connections for each vertex.
    2. Total number of vertices.
    3. Sum of degrees for all vertices.

    Perfect input is assumed.
    """
    def __init__(self):
        self.edge_set = defaultdict(set) 
        self.num_vertices = 0
        self.num_degrees = 0

    def add_edge(self,x,y):
        """
        This method adds an edge that connects vertices x and y
        and subsequently updates relevant fields.

        If the vertices are new then the total number of vertices
        is incremented for each new vertex.

        The sum of degrees is incemented by 2.
        
        Assumes that the edge does not already exist.
        
        """
        if len(self.edge_set[x]) == 0:
            self.num_vertices += 1
        if len(self.edge_set[y]) == 0:
            self.num_vertices += 1
        self.edge_set[x].add(y)
        self.edge_set[y].add(x)
        self.num_degrees += 2
    def remove_edge(self,x,y):
        """
        This method removes an edge that connects x and y.
        For the purposes of this exercise the relevant edge and 
        the relevant vertices must exist.

        The class members are updated accordingly.

        The sum of degrees is decremented by 2
        and x and y are removed from each other's edge sets.

        If a vertex has no more connections then the number of vertices
        is decremented by 1 for each such vertex.

        This method assumes that both x and y exist as vertices and there 
        is an edge between them.
        """
        edge = frozenset([x,y])
        self.num_degrees -= 2
        self.edge_set[x].remove(y)
        self.edge_set[y].remove(x)
        if len(self.edge_set[x]) == 0:
            self.num_vertices -= 1
            self.edge_set.pop(x)
        if len(self.edge_set[y]) == 0:
            self.num_vertices -= 1
            self.edge_set.pop(y)
    def get_ave(self):
        """
        This method returns the average degree.
        """
        if self.num_vertices > 0:
            return 1.0 * self.num_degrees / self.num_vertices 
        else:
            return 0
