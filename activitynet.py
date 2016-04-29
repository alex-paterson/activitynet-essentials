'''
This file contains helper methods relevant to reading the ActivityNet JSON files
and parsing their data. The paths to the files are defined in __init__.py of
this package
'''

import json, sys, os
from . import ROOT_DIR

SPACE = '    ' # For printing purposes
JSON_V2_PATH = os.path.join(ROOT_DIR, "./activity_net.v1-2.min.json")
JSON_V3_PATH = os.path.join(ROOT_DIR, "./activity_net.v1-3.min.json")


'''
Generic helpers
'''
# Determines if value is a string, version independent
def isstring(s):
    if (sys.version_info[0] == 3):
        return isinstance(s, str)
    return isinstance(s, basestring)

def print_list(l):
    for d in l:
        print(d)


'''
Tree Datastructure
'''

# Iterates over a list of dictionaries matching 'parentName' key's value
# returns list of matches
def get_dictionaries_with_parent_name(list_of_dictionaries, parent_name):
    nodes_with_parent = []
    for node in list_of_dictionaries:
        if node['parentName'] == parent_name:
            nodes_with_parent.append(node)
    return nodes_with_parent

# Recursively constructs tree
def get_child_tree(taxonomy_json, nodeName):
    children = get_dictionaries_with_parent_name(taxonomy_json, nodeName)
    child_tree = [ get_child_tree(taxonomy_json, x['nodeName']) for x in children ]
    return_dict = {nodeName: child_tree} if child_tree else nodeName
    return return_dict

# Recursively prints trees. Can be passed a dictionary or a list
def print_child_tree(tree_list, depth):
    if tree_list == []:
        return
    elif isinstance(tree_list, dict):
        for key in tree_list:
            print(SPACE*depth + key)
            print_child_tree(tree_list[key], depth+1)
    else:
        for tree in tree_list:
            if isstring(tree):
                print(SPACE*depth + tree)
            else:
                for key in tree:
                    print(SPACE*depth + key)
                    print_child_tree(tree[key], depth+1)




'''
ActivityNet
'''


class ActivityNet:

    def __init__(this, version):
        if version == 2:
            this.json_net = this.get_json_v2()
        elif verison == 3:
            this.json_net = this.get_json_v3()
        else:
            raise ValueError("ActivityNet must be initialized as verison 2 or 3")


    '''
    JSON File I/O
    '''
    # Reads the ActivityNet JSON files and returns as python dictionary.
    # Define paths to these files in __init__.py
    def get_json_v2(this):
        print("Loading ActivityNet Version 2")
        return json.load(open(JSON_V2_PATH))

    def get_json_v3(this):
        print("Loading ActivityNet Version 3")
        return json.load(open(JSON_V3_PATH))


    '''
    Taxonomy
    '''

    # Simple wrapper for get_child_tree. Pass ActivityNet JSON, returns taxonomy
    # tree starting at root
    def get_taxonomy_tree(this):
        return get_child_tree(this.json_net['taxonomy'], 'Root')

    # Wrapper for everything to print the taxonomy tree of an ActivityNet JSON
    # object
    def print_taxonomy_tree(this):
        print_child_tree(this.get_taxonomy_tree(), 0)


    '''
    Database
    '''

    # Get set of nodes by subset {'testing', 'training', 'validation'}
    # in form: [{u'duration': 92.18, u'subset': u'training', ... }, ...]
    def get_subset(this, subset):
        node_set = []
        database = this.json_net['database']
        for key in database:
            node = database[key]
            if node['subset'] == subset:
                node_set.append(node)
        return node_set

    # Counts items with a particular label
    def count_items_with_label(this, label):
        count = 0
        database = this.json_net['database']
        for key in database:
            node = database[key]
            for annotation in node['annotations']:
                if annotation['label'] == label:
                    count += 1
                    break
        return count

    # Returns items with a particular label as a list of dictionaries
    # in form: [{u'duration': 92.18, u'subset': u'training', ... }, ...]
    def get_items_with_label(this, label):
        items = []
        database = this.json_net['database']
        for key in database:
            node = database[key]
            for annotation in node['annotations']:
                if annotation['label'] == label:
                    items.append(node)
                    break
        return items

    # Returns items in a subset with a particular label
    # in form: [{u'duration': 92.18, u'subset': u'training', ... }, ...]
    def get_subset_with_label(this, subset, label):
        items = []
        database = this.json_net['database']
        for key in database:
            node = database[key]
            if node['subset'] == subset:
                for annotation in node['annotations']:
                    if annotation['label'] == label:
                        items.append(node)
                        break
        return items

    @staticmethod
    def count_annotations_from_node(node):
        count = 0
        for annotation in node['annotations']:
            count +=1
        return count

    @staticmethod
    def get_annotations_from_node(node):
        annotations = []
        for annotation in node['annotations']:
            annotations.append(annotation)
        return annotations
