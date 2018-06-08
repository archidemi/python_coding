
### Question 1
Given two strings `s` and `t`, determine whether some anagram of `t` is a substring of `s`. For example: if `s = "udacity"` and `t = "ad"`, then the function returns `True`. Your function definition should look like: `question1(s, t)` and return a boolean `True` or `False`.


```python
from collections import Counter

def question1(s, t):
    if (len(s) < len(t)) or (len(s) * len(t) == 0):
        return False
    delta = get_letter_differences(s[:len(t)], t)
    i = 0
    while(len(delta) != 0 and i < len(s) - len(t)):
        if s[i] in delta and delta[s[i]] == 1:
            del delta[s[i]]
        elif s[i] in delta:
            delta[s[i]] -= 1
        else:
            delta[s[i]] = -1
        if s[len(t) + i] in delta and delta[s[len(t) + i]] == -1:
            del delta[s[len(t) + i]]
        elif s[len(t) + i] in delta:
            delta[s[len(t) + i]] += 1
        else:
            delta[s[len(t) + i]] = 1
        i += 1
    if len(delta) == 0:
        return True
    return False

def get_letter_differences(s1, s2):
    c1 = dict(Counter(s1))
    c2 = dict(Counter(s2))
    delta = {}
    for key in c1:
        if key in c2 and c1[key] != c2[key]:
            delta[key] = c1[key] - c2.pop(key)
        elif key in c2 and c1[key] == c2[key]:
            del c2[key]
        else:
            delta[key] = c1[key]
    for key in c2:
        delta[key] = -c2[key]
    return delta
```

This is a "sliding window" solution. I created a dictionary as a counter to store the elements as keys, and their number of appearance as values. I came up with this data structure intuitively. We have to go through the string only once to get it (O(n)). A helper function is defined to calculate the difference of two "counter dictionaries". In worst case, each character appears only once, no overlap between the two strings, so we go through both string once (O(n)). By moving one position toward the right at a time until we find the substring, the worst case is again O(n).

The time efficiency is O(n).  
The space efficiency is O(n).  
n is the sum of the length of the two strings.

---

### Question 2
Given a string `a`, find the longest palindromic substring contained in `a`. Your function definition should look like `question2(a)`, and return a string.


```python
def question2(a):
    p = ''
    if len(a) < 2:
        return a

    elif a[0] == a[-1]:
        rec = question2(a[1:-1])
        if len(rec) == len(a[1:-1]):
            p = a
        else:
            p = rec

    else:
        notail = question2(a[:-1])
        nohead = question2(a[1:])
        if len(notail) < len(nohead):
            return nohead
        else:
            return notail
        # return the first palindromic substring if multiple ones with the same length
    return p
```

This is a very time and space costly solution, but with only a few lines and intuitive thinking. In the n'th recursion, 2^n substrings are created, until only one or two elements are left.

The time efficiency is O(2^n).  
The space efficiency is O(2^1*(n-1) + 2^2*(n-2) + ... + 2^(n-1)*1), approximately O(n*2^n).  
n is the length of the string.

---

### Question 3
Given an undirected graph G, find the minimum spanning tree within G. A minimum spanning tree connects all vertices in a graph with the smallest possible total weight of edges. Your function should take in and return an adjacency list structured like this:
```python
{'A': [('B', 2)],
 'B': [('A', 2), ('C', 5)], 
 'C': [('B', 5)]}
```
Vertices are represented as unique strings. The function definition should be `question3(G)`


```python
# first solution
def question3(G):
    distance = {}
    tree = {}
    for key in G:
        distance[key] = (key, float('inf'))
        tree[key] = []
    current = pop_min_point(distance)
    
    while(len(distance) != 0):
        for edge in G[current[0]]:
            if (edge[0] in distance) and (edge[1] < distance[edge[0]][1]):
                distance[edge[0]] = (current[0], edge[1])
        current = pop_min_point(distance)
        if current[2] == float('inf'):
            # means we encounter a disconnected point
            break
        tree[current[0]].append((current[1], current[2]))
        tree[current[1]].append((current[0], current[2]))
    
    if all(tree.values()):
        return tree
    return "The graph is not connected. The minimum spanning tree doesn't exist."

def pop_min_point(dict):
    min = (dict.keys()[0], dict.values()[0][0], dict.values()[0][1])
    for key in dict:
        if dict[key][1] < min[2]:
            min = (key, dict[key][0], dict[key][1])
    del dict[min[0]]
    return min
```


```python
# better solution
from heapq import heappush, heappop

def question3(G):
    h = []
    tree = {}
    for key in G:
        heappush(h, (float('inf'), key, key))
    current = heappop(h)
    
    while(len(tree) < len(G)):
        for edge in G[current[1]]:
            if (edge[0] not in tree):
                heappush(h, (edge[1], edge[0], current[1]))
        current = heappop(h)
        if current[1] in tree:
            current = heappop(h)
        if current[0] == float('inf'):
            break
        tree[current[1]] = [(current[2], current[0])]
        if current[2] in tree:
            tree[current[2]].append((current[1], current[0]))
        else:
            tree[current[2]] = [(current[1], current[0])]
        
    if len(tree) == len(G):
        return tree
    return "The graph is not connected. The minimum spanning tree doesn't exist."
```

This solution utilizes the `heapq` package. A list of tuples is used to store the edge weights, two vertices that are connected by the edge, and to pop the current minimum edge. Whenever a new closest vertex is found, it is added to the output dictionary. When initializing the list, every vertex is "pushed" (O(V)). Every edge from each vertex is checked in this algorithm (O(E+V)).

The time efficiency is O(E+2V), approximately O(E+V).  
The space complexity is O(E+2V), also O(E+V).  
E is the number of edges. V is the number of vertices.

---

### Question 4
Find the least common ancestor between two nodes on a binary search tree. The least common ancestor is the farthest node from the root that is an ancestor of both nodes. For example, the root is a common ancestor of all nodes on the tree, but if both nodes are descendents of the root's left child, then that left child might be the lowest common ancestor. You can assume that both nodes are in the tree, and the tree itself adheres to all BST properties. The function definition should look like `question4(T, r, n1, n2)`, where `T` is the tree represented as a matrix, where the index of the list is equal to the integer stored in that node and a `1` represents a child node, `r` is a non-negative integer representing the root, and `n1` and `n2` are non-negative integers representing the two nodes in no particular order. For example, one test case might be
```python
question4([[0, 1, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [0, 0, 0, 0, 0],
           [1, 0, 0, 0, 1],
           [0, 0, 0, 0, 0]],
          3,
          1,
          4)
```
and the answer would be `3`.


```python
def question4(T, r, n1, n2):
    parent = r
    if sidedness(parent, n1, n2) == True:
        for i in range(len(T)):
            if T[parent][i] == 1 and sidedness(parent, i, n1) == True:
                return question4(T, i, n1, n2)
    if n1 == parent:
        parent = n1
    if n2 == parent:
        parent = n2
    return parent

def sidedness(parent, child1, child2):
    if (child1 - parent) * (child2 - parent) > 0:
        return True
    else:
        return False
```
We are trying to find the first node that n1 and n2 are on different sides of that node. The worst case would be an unbalanced tree with n1 and n2 at the end. In each recursion, the children of the current parent is checked by going through the "row" of the matrix. So it's O(n) in O(n), which is O(n^2).

The time efficiency is O(nn).  
The space efficiency is O(n), since the parent of each recursion is temporarily stored in the stack when going down the tree.

---

### Question 5
Find the element in a singly linked list that's `m` elements from the end. For example, if a linked list has 5 elements, the 3rd element from the end is the 3rd element. The function definition should look like `question5(ll, m)`, where `ll` is the first node of a linked list and `m` is the "mth number from the end". You should copy/paste the `Node` class below to use as a representation of a node in the linked list. Return the value of the node at that position.
```python
class Node(object):
  def __init__(self, data):
    self.data = data
    self.next = None
```


```python
class Node(object):
    def __init__(self, data):
        self.data = data
        self.next = None
    
def question5(ll, m):
    ruler =[ll, None]
    current = ll
    counter = 1
    while(current):
        if counter == m:
            ruler[1] = current
            
        if counter > m:
            ruler[0] = ruler[0].next
            ruler[1] = current
            
        current = current.next
        counter += 1
    if ruler[1]:
        return ruler[0].data
    return 'm is longer than the linked list.'
```
The first thought was creating a queue as a ruler of length m to move from the head to the tail of the linked list. But actually only the beginning and the end of the ruler are necessary. So we merely have to go through the linked list once, and two values are stored and updated.

The time efficiency is O(n).  
The space efficiency is O(1).
