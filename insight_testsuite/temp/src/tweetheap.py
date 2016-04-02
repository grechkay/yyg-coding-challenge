
class TweetHeap:
    """
    Heap customized for the problem to store tweets.
    Algorithms are mainly coppied from the python source file for heapq at
    https://hg.python.org/cpython/file/3.4/Lib/heapq.py

    Slight modifications are made to change priorities when necessary; this 
    is used in order to change the times of duplicate edges when new ones 
    arrive.
    """
    def __init__(self):
        """
        The heap entries will be in the form of tuples (timestamp, frozenset(hashtag1, hashtag2))
        The edgehash keys will be frozenset(hashtag1, hashtag2), the items will be heap indeces.
        """
        self.heap = []
        self.edgehash = {}
    def _siftdown(self,startpos,pos):
        """
        Workhorse method to bubble an element up the heap.

        Follows the source code for the identical method of the heapq module.
        Adds logic to update the edgehash.
        """
        newitem = self.heap[pos]
        while pos > startpos:
            parentpos = (pos - 1) >> 1
            parent = self.heap[parentpos]
            edge = parent[1] 
            if newitem < parent:
                self.heap[pos] = parent
                self.edgehash[edge] = pos
                
                pos = parentpos
                continue
            break
        self.heap[pos] = newitem
        newitem_edge = newitem[1]
        self.edgehash[newitem_edge] = pos
    
    def _siftup(self,pos):
        """
        Workhorse method to bubble an element down the heap.

        Follows the source code for the identical method of the heapq module.
        Adds logic to update the edgehash.
        """
        endpos = len(self.heap)
        startpos = pos
        newitem = self.heap[pos]
        childpos = 2*pos + 1
        while childpos < endpos:
            rightpos = childpos + 1
            if rightpos < endpos and not self.heap[childpos] < self.heap[rightpos]:
                childpos = rightpos
            child = self.heap[childpos]
            child_edge = child[1]
            self.heap[pos] = child
            self.edgehash[child_edge] = pos
            
            pos = childpos
            childpos = 2*pos + 1
        self.heap[pos] = newitem
        newitem_edge = newitem[1]
        self.edgehash[newitem_edge] = pos
        self._siftdown(startpos,pos)

    
    def push(self,item):
        """
        Method to push an element onto the heap while keeping the heap invariant.
        Follows the source code of the heappush function of the heapq module.

        Adds logic to update the edgehash and to change the priority when an identical
        element is inserted.
        """
        timestamp = item[0]
        key = item[1]
        heappos = self.edgehash.get(key)
        if heappos is not None:
            edge_timestamp = self.heap[heappos][0]
            if edge_timestamp < timestamp:
                self.heap[heappos] = item
                self._siftup(heappos)
            else:
                return
        else:
            pos = len(self.heap)
            self.heap.append(item)
            self.edgehash[key] = pos

            self._siftdown(0,pos)
        
    def pop(self):
        """
        Method to pop off the lowest timestamp element off the heap
        while keeping the heap invariant. Follows the source code of the heappush
        function of the heapq module.

        Adds logic to update the edgehash.
        """

        lastelt = self.heap.pop()
        key = lastelt[1]
        if self.heap:
            returnitem = self.heap[0]
            self.edgehash[key] = 0
            self.edgehash.pop(returnitem[1])
            self.heap[0] = lastelt
            self._siftup(0)
        else:
            self.edgehash.pop(key)
            returnitem = lastelt
        return returnitem
        
        

