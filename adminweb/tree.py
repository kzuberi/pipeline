import os
from configobj import ConfigObj


class TreeNode(object):
    """Node of a tree in the UI treeview, fields as required
    by fancytree plugin. subclasses adding application
    specific fields.

    icon field is a bit weird, since it can be a string
    or boolean
    """
    def __init__(self):
        self.title = ''
        self.folder = False
        self.icon = ''
        self.children = []
        self.key = ''

        self.type = None

    def add_child(self, node):
        self.children.append(node)

    def add_children(self, node_list):
        self.children.extend(node_list)

    def as_dict(self):
        return vars(self)


class OrganismTreeNode(TreeNode):
    def __init__(self, cfg):
        self.id = ''
        self.name = ''
        self.code = ''

        self.folder = True
        self.type = 'organism'
        self.key = 'o=%s' % self.id


class NetworkTreeNode(TreeNode):
    def __init__(self, cfg):
        pass


class TreeLoader:
    def __init__(self, data_folder):
        self.data_folder = data_folder

    def organism(self):
        filename = os.path.join(self.data_folder, 'organism.cfg')
        cfg = ConfigObj(filename, encoding='UTF8')

        node = OrganismTreeNode(cfg)
        return node




