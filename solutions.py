# Question 1

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

###################################

# Question 2

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
        """Return the first palindromic substring if multiple ones with the same length."""
    return p

###################################

# Question 3

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

###################################

# Question 4

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

###################################

# Question 5

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

###################################

# test

import unittest

class Test(unittest.TestCase):

    def test_question1(self):
        self.assertFalse(question1('abc', ''))
        self.assertFalse(question1('', 'aaa'))
        self.assertFalse(question1('abc', 'abcde'))
        self.assertTrue(question1('abcdefg', 'dfgcbae'))
        self.assertTrue(question1('abcdefgllqqq', 'dfgcbae'))
        self.assertTrue(question1(';sdlkfjds;', 'kfl'))

    def test_question2(self):
        self.assertEqual(question2(''), '')
        self.assertEqual(question2('z'), 'z')
        self.assertEqual(question2('bab'), 'bab')
        self.assertEqual(question2('amom'), 'mom')
        self.assertEqual(question2('bamomb'), 'mom')
        self.assertEqual(question2('zzbabab'), 'babab')
        self.assertEqual(question2('bababzz'), 'babab')
        self.assertEqual(question2('cdadzzmomc'), 'dad')

    def test_question3(self):
        G = {'A': [('B', 1), ('C', 7)],
             'B': [('A', 1), ('C', 2)],
             'C': [('A', 7), ('B', 2)]}
        out = {'A': [('B', 1)], 'B': [('A', 1), ('C', 2)], 'C': [('B', 2)]}
        self.assertEqual(question3(G), out)
        G = {'A': [('B', 1), ('C', 7)],
             'B': [('A', 1), ('C', 2)],
             'C': [('A', 7), ('B', 2)],
             'D': []}
        out = "The graph is not connected. The minimum spanning tree doesn't exist."
        self.assertEqual(question3(G), out)
        G = {'A': [('B', 8), ('C', 7), ('E', 2)],
             'B': [('A', 8), ('C', 4), ('D', 5)],
             'C': [('A', 7), ('B', 4), ('D', 1), ('E', 6)],
             'D': [('B', 5), ('C', 1), ('E', 3)],
             'E': [('A', 2), ('C', 6), ('D', 3)]}
        out = {'A': [('E', 2)], 'C': [('D', 1), ('B', 4)], 'B': [('C', 4)], 'E': [('A', 2), ('D', 3)], 'D': [('E', 3), ('C', 1)]}
        self.assertEqual(question3(G), out)

    def test_question4(self):
        T = [[0, 1, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [1, 0, 0, 0, 1],
             [0, 0, 0, 0, 0]]
        self.assertEqual(question4(T, 3, 1, 4), 3)
        T = [[0, 0, 0, 0, 0],
             [1, 0, 0, 0, 0],
             [0, 1, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0]]
        self.assertEqual(question4(T, 2, 1, 0), 1)
        T = [[0, 0, 0, 0, 0],
             [1, 0, 0, 0, 0],
             [0, 1, 0, 1, 0],
             [0, 0, 0, 0, 1],
             [0, 0, 0, 0, 0]]
        self.assertEqual(question4(T, 2, 0, 4), 2)
        T = [[0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 1, 0],
             [0, 0, 0, 0, 1],
             [0, 0, 0, 0, 0]]
        self.assertEqual(question4(T, 2, 3, 4), 3)
        T = [[0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 1, 0, 1, 0],
             [0, 0, 0, 0, 1],
             [0, 0, 0, 0, 0]]
        self.assertEqual(question4(T, 2, 3, 4), 3)

    def test_question5(self):
        ll = Node(1)
        ll.next = Node(2)
        ll.next.next = Node(3)
        ll.next.next.next = Node(4)
        ll.next.next.next.next = Node(5)
        self.assertEqual(question5(ll, 1), 5)
        self.assertEqual(question5(ll, 3), 3)
        self.assertEqual(question5(ll, 7), 'm is longer than the linked list.')
        ll = Node(1)
        self.assertEqual(question5(ll, 1), 1)
        self.assertEqual(question5(ll, 2), 'm is longer than the linked list.')
        ll = None
        self.assertEqual(question5(ll, 3), 'm is longer than the linked list.')
        
if __name__ == '__main__':
    unittest.main(argv=['ignored', '-v'], exit=False)