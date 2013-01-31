#!/usr/bin/env python

""" Test suite for GsmTerm """

import unittest

import gsmterm.trie

class TestTrie(unittest.TestCase):
    """ Tests the trie implementation used by GsmTerm """    
    
    def setUp(self):        
        self.trie = gsmterm.trie.Trie()
        self.keyValuePairs = (('abc', 'def'),
                         ('hallo', 'daar'),
                         ('hoe gaan', 'dit met jou'),
                         ('sbzd', '123'),
                         ('abcde', '234627sdg'),
                         ('ab', 'asdk;jgdjsagkl'))
    
    def test_storeSingle(self):
        """ Tests single key/value pair storage """        
        self.trie['hallo'] = 'daar'        
        self.assertEqual(self.trie['hallo'], 'daar')
        self.assertEqual(len(self.trie), 1)
        self.assertRaises(KeyError, self.trie.__getitem__, 'abc')
        
    def test_storeRetrieveMultiple(self):
        n = 0
        for key, value in self.keyValuePairs:
            n += 1
            self.trie[key] = value
            self.assertEqual(self.trie[key], value)            
            # Make sure nothing was lost
            for oldKey, oldValue in self.keyValuePairs[:n-1]:
                self.assertEqual(self.trie[oldKey], oldValue)
    
    def test_len(self):
        n = 0
        for key, value in self.keyValuePairs:
            n += 1
            self.trie[key] = value
            self.assertEqual(len(self.trie), n, 'Incorrect trie length. Expected {0}, got {1}. Last entry: {2}: {3}'.format(n, len(self.trie), key, value))
    
    def test_keys(self):
        """ Test the "keys" method of the trie """
        localKeys = []
        for key, value in self.keyValuePairs:
            localKeys.append(key)
            self.trie[key] = value
        # The trie has no concept of ordering, so we can't simply compare keys with ==
        trieKeys = self.trie.keys()
        self.assertEquals(len(trieKeys), len(localKeys))
        for key in localKeys:
            self.assertTrue(key in trieKeys)
    
    def test_overWrite(self):
        # Fill up trie with some values
        for key, value in self.keyValuePairs:            
            self.trie[key] = value
        key, oldValue = self.keyValuePairs[0]
        length = len(self.keyValuePairs)
        self.assertEqual(self.trie[key], oldValue)
        self.assertEqual(len(self.trie), length)
        # Overwrite value
        newValue = oldValue + '12345'
        self.assertNotEqual(oldValue, newValue)
        self.trie[key] = newValue
        # Read it back
        self.assertEqual(self.trie[key], newValue)
        # Check trie length is unchanged
        self.assertEqual(len(self.trie), length)
    
    def test_filteredKeys(self):
        """ Test the "matching keys" functionality of the trie """
        keys = ('a', 'ab', 'abc', 'abcd0000', 'abcd1111', 'abcd2222', 'abcd3333', 'b000', 'b1111', 'zzz123', 'zzzz1234', 'xyz123')
        prefixMatches = (('abc', [key for key in keys if key.startswith('abc')]),
                         ('b', [key for key in keys if key.startswith('b')]),
                         ('bc', [key for key in keys if key.startswith('bc')]),
                         ('zzz', [key for key in keys if key.startswith('zzz')]),
                         ('x', [key for key in keys if key.startswith('x')]),
                         ('xy', [key for key in keys if key.startswith('xy')]),
                         ('qwerty', [keys for key in keys if key.startswith('qwerty')]))        
        for key in keys:
            self.trie[key] = 1
        for prefix, matchingKeys in prefixMatches:
            trieKeys = self.trie.keys(prefix)
            self.assertEqual(len(trieKeys), len(matchingKeys), 'Filtered keys length failed. Prefix: {}, expected len: {}, items: {}, got len {}, items: {}'.format(prefix, len(matchingKeys), matchingKeys, len(trieKeys), trieKeys))
            for key in matchingKeys:
                self.assertTrue(key in trieKeys, 'Key not in trie keys: {0}. Trie keys: {1}'.format(key, trieKeys))
       
if __name__ == "__main__":
    unittest.main()