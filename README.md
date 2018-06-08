
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


```python
# test cases

s1 = 'abc'
t1 = ''
print question1(s1, t1)
# should print "False"

s2 = ''
t2 = 'aaa'
print question1(s2, t2)
# should print "False"

s3 = 'abc'
t3 = 'abcde'
print question1(s3, t3)
# should print "False"

s4='abcdefg'
t4='dfgcbae'
print question1(s4, t4)
# should print "True"

s5='abcdefgllqqq'
t5='dfgcbae'
print question1(s5, t5)
# should print "True"

s6 = ';sdlkfjds;'
t6 = 'kfl'
print question1(s6, t6)
# should print "True"
```

    False
    False
    False
    True
    True
    True


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


```python
a = ''
print question2(a)
# should print nothing (None)

a = 'z'
print question2(a)
# should print 'z'

a = 'bab'
print question2(a)
# should print 'bab'

a = 'amom'
print question2(a)
# should print 'mom'

a = 'bamomb'
print question2(a)
# should print 'mom'

a = 'zzbabab'
print question2(a)
# should print 'babab'

a = 'bababzz'
print question2(a)
# should print 'babab'

a = 'cdadzzmomc'
print question2(a)
# should print 'dad'
```

    
    z
    bab
    mom
    mom
    babab
    babab
    dad


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


```python
# test case

G = {'A': [('B', 1), ('C', 7)],
     'B': [('A', 1), ('C', 2)],
     'C': [('A', 7), ('B', 2)]}
print question3(G)
# should print {'A': [('B', 1)], 'B': [('A', 1), ('C', 2)], 'C': [('B', 2)]}

G = {'A': [('B', 1), ('C', 7)],
     'B': [('A', 1), ('C', 2)],
     'C': [('A', 7), ('B', 2)],
     'D': []}
print question3(G)
# should print "The graph is not connected. The minimum spanning tree doesn't exist."

G = {'A': [('B', 8), ('C', 7), ('E', 2)],
     'B': [('A', 8), ('C', 4), ('D', 5)],
     'C': [('A', 7), ('B', 4), ('D', 1), ('E', 6)],
     'D': [('B', 5), ('C', 1), ('E', 3)],
     'E': [('A', 2), ('C', 6), ('D', 3)]}
print question3(G)
# should print
# {'A': [('E', 2)], 'C': [('D', 1), ('B', 4)], 'B': [('C', 4)], 'E': [('A', 2), ('D', 3)], 'D': [('E', 3), ('C', 1)]}
```

    {'A': [('B', 1)], 'C': [('B', 2)], 'B': [('A', 1), ('C', 2)]}
    The graph is not connected. The minimum spanning tree doesn't exist.
    {'A': [('E', 2)], 'C': [('D', 1), ('B', 4)], 'B': [('C', 4)], 'E': [('A', 2), ('D', 3)], 'D': [('E', 3), ('C', 1)]}


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


```python
T = [[0, 1, 0, 0, 0],
     [0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0],
     [1, 0, 0, 0, 1],
     [0, 0, 0, 0, 0]]
print question4(T, 3, 1, 4)
# should print 3

T = [[0, 0, 0, 0, 0],
     [1, 0, 0, 0, 0],
     [0, 1, 0, 0, 0],
     [0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0]]
print question4(T, 2, 1, 0)
# should print 1

T = [[0, 0, 0, 0, 0],
     [1, 0, 0, 0, 0],
     [0, 1, 0, 1, 0],
     [0, 0, 0, 0, 1],
     [0, 0, 0, 0, 0]]
print question4(T, 2, 0, 4)
# should print 2

T = [[0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0],
     [0, 0, 0, 1, 0],
     [0, 0, 0, 0, 1],
     [0, 0, 0, 0, 0]]
print question4(T, 2, 3, 4)
# should print 3

T = [[0, 0, 0, 0, 0],
     [0, 0, 0, 0, 0],
     [0, 1, 0, 1, 0],
     [0, 0, 0, 0, 1],
     [0, 0, 0, 0, 0]]
print question4(T, 2, 3, 4)
# should print 3
```

    3
    1
    2
    3
    3


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


```python
# test cases

ll = Node(1)
ll.next = Node(2)
ll.next.next = Node(3)
ll.next.next.next = Node(4)
ll.next.next.next.next = Node(5)

print question5(ll, 1)
# should return 5

print question5(ll, 3)
# should return 3

print question5(ll, 7)
# should return "m is longer than the linked list."

ll = Node(1)

print question5(ll, 1)
# should print 1

print question5(ll, 2)
# should return "m is longer than the linked list."

ll = None

print question5(ll, 3)
# should return "m is longer than the linked list."
```

    5
    3
    m is longer than the linked list.
    1
    m is longer than the linked list.
    m is longer than the linked list.
