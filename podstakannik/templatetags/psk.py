import re
from django import template
from ..models import Page

page_tree_re = re.compile(r"\[PAGE_TREE:? *([^\]]*)\]")

register = template.Library()

def make_page_tree(fn):
    def sub_repl(m):
        url = m.group(1)
        p = Page.objects.get(url=url)
        return fn(fn, p)
    def dj_filter(value):
        orig = str(value)
        try:
            return page_tree_re.sub(sub_repl, orig)
        except:
            return orig
    
    return register.filter(fn.__name__, dj_filter)

@make_page_tree
def markdown_page_tree(fn, p, indent=0):
    ret = "    " * indent
    
    if p.subtitle:
        ret += " * [%s](%s) - %s\n" % (p.title, p.get_absolute_url(), p.subtitle)
    else:
         ret += " * [%s](%s)\n" % (p.title, p.get_absolute_url())       
         
    for child in p.get_children():
        ret += fn(fn, child, indent + 1)
    
    return ret
