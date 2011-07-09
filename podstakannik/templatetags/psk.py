import re
from django import template
from ..models import Page, File

try:
    import markdown
except ImportError:
    markdown = None

def markdown_page_tree(p, indent=0):
    ret = "    " * indent
    
    if p.subtitle:
        ret += " * [%s](%s) - %s\n" % (p.title, p.get_absolute_url(), p.subtitle)
    else:
         ret += " * [%s](%s)\n" % (p.title, p.get_absolute_url())       
         
    for child in p.get_children():
        ret += markdown_page_tree(child, indent + 1)
    
    return ret

# match rules used in psk
# format: (compiled_re, typelist, functiondict)
#
# typelist is a list of strings, which are indexes into convert (see below)
#
# functiondict is a mapping of fmt names into functions, which should
# accept the same number of arguments as there are match groups, and should
# return a string used to replace the whole match
rules = [
    (re.compile(r"\[PAGE_TREE:? *([^\]]*)\]"),
     ('page',), {
            'markdown' : markdown_page_tree,
    }),

    (re.compile(r"\[FILEMD5:? *([^\]]*)\]"),
     ('file',), {'all' : lambda f: f.md5}),
    (re.compile(r"\[FILESIZE:? *([^\]]*)\]"),
     ('file',), {'all' : lambda f: f.nice_size}),
    (re.compile(r"\[FILE:? *([^\]]*)\]"),
     ('file',), {'all' : lambda f: f.get_absolute_url()}),
]

# functions for turning a regex match into a useful object
# given the page and the match string
def convert_page(p, s):
    if s:
        return Page.objects.get(url=s)
    return p
def convert_file(p, s):
    if " " in s:
        url, name = s.split(" ", 1)
    else:
        url = p.url
        name = s
    return File.objects.get(parent__url=url, name=name)
convert = {
    'page' : convert_page,
    'file' : convert_file,
}

# functions for doing the final conversion, by fmt name
final = {
    # FIXME make extensions configurable
    'markdown' : lambda s: markdown.markdown(s, ['extra', 'toc', 'codehilite']),
}

register = template.Library()

@register.filter
def psk(value, p):
    fmt = 'markdown'
    s = str(value)
    
    for regex, types, fnmap in rules:
        def sub_repl(m):
            args = []
            for i, typ in enumerate(types):
                typ = convert.get(typ, lambda s: str(s))
                val = m.group(i + 1)
                if val is None:
                    args.append(val)
                    continue
                try:
                    args.append(typ(p, val))
                except:
                    return ''
            rule = fnmap.get(fmt, fnmap.get('all', None))
            if rule is None:
                return ''
            try:
                return rule(*args)
            except:
                return ''
        s = regex.sub(sub_repl, s)
    
    if fmt in final:
        try:
            return final[fmt](s)
        except:
            pass
    
    return s
