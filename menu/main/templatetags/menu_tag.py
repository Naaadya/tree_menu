from django import template
from ..models import Menu

class tree_item:
    def __init__(self, name, url, id, parent_id, selected = False):
        self.name = name
        self.url = url
        self.children = []
        self.id = id
        self.parent_id = parent_id
        self.selected = selected
    def addChild(self, child):
        self.children.append(child)
        child.parent = self
    

def dfs(node, url):
    if node.url == url:
        node.selected = True
        return node
    for c in node.children:
        res = dfs(c, url)
        if res:
            return res
#убираем ненужные элементы из дерева 
def copy_tree(node, url):
    node_copy = tree_item(node.name, node.url, node.id, node.parent_id, node.selected)
    for c in node.children:
        if dfs(c, url):
            node_copy.addChild(copy_tree(c, url))
        else:
            node_copy.addChild(tree_item(c.name, c.url, c.id, c.parent_id, c.selected))
    return node_copy


def find_db_item(db_items, parent_id):
    for item in db_items:
        if item.parent_id == parent_id:
            return item
    return None

#строим дерево из бд
def build_tree(db_items, parent_html):
    for item in db_items:
        if item.parent_id == parent_html.id:
            html_item = tree_item(item.name, item.url, item.id, item.parent_id)
            parent_html.addChild(html_item)
            build_tree(db_items, html_item)
    return parent_html

def get_data(type, url):


    items = Menu.objects.filter(type=type)
    
    db_root = find_db_item(items, None)
    html_items = build_tree(items, tree_item(db_root.name, db_root.url, db_root.id, db_root.parent_id, False))

    #in-memory тесты
    #root = tree_item('root', '', None, None)
    #item1 = tree_item('item1', '/item1/', None, None)
    #item1.addChild(tree_item('item1_1', '/item1/item1_1/', None, None))
    #item1_2 = tree_item('item1_2', '/item1/item1_2/', None, None)
    #item1_2.addChild(tree_item('item1_2_1', '/item1/item1_2/item1_2_1/', None, None))
    #item1_2.addChild(tree_item('item1_2_2', '/item1/item1_2/item1_2_2/', None, None))
    #item1_2.addChild(tree_item('item1_2_3', '/item1/item1_2/item1_2_3/', None, None))
    #item1.addChild(item1_2)
    #item1.addChild(tree_item('item1_3', '/item1/item1_3/', None, None))
    #root.addChild(item1)
    #item2 = tree_item('item2', '/item2/', None, None)
    #item2.addChild(tree_item('item2_1', '/item2/item2_1/', None, None))
    #item2.addChild(tree_item('item2_2', '/item2/item2_2/', None, None))
    #item2.addChild(tree_item('item2_3', '/item2/item2_3/', None, None))
    #root.addChild(item2)
    #item3 = tree_item('item3', '/item3/', None, None)
    #item3.addChild(tree_item('item3_1', '/item3/item3_1/', None, None))
    #item3.addChild(tree_item('item3_2', '/item3/item3_2/', None, None))
    #item3.addChild(tree_item('item3_3', '/item3/item3_3/', None, None))
    #root.addChild(item3)

    return html_items

register = template.Library()
@register.inclusion_tag('main/menu.html', takes_context=True)
def draw_menu(context, name):
    url = context['request'].path
    root = get_data(name, url)
    copy = copy_tree(root, url)
    return {"root": copy}