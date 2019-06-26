from jinja2 import Markup

def format_unixtime(unixtime):
    raw_html = "<script>\ndocument.write(moment.unix(\"%s\").calendar());\n</script>"
    html = raw_html % unixtime
    return Markup(html)
