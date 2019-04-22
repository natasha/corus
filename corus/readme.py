
import re

from .io import (
    load_text,
    dump_text
)


DOCS = 'https://nbviewer.jupyter.org/github/natasha/corus/blob/master/docs.ipynb'


def format_metas_(metas):
    yield '<table>'
    yield '<tr>'
    yield '<th>Dataset</th>'
    yield '<th>API <code>from corus import</code></th>'
    yield '<th>Description</th>'
    yield '</tr>'
    for meta in metas:
        yield '<tr>'

        yield '<td>'
        yield '<a href="%s">%s</a>' % (meta.url, meta.title)
        yield '</td>'

        yield '<td>'
        for index, function in enumerate(meta.functions):
            if index > 0:
                yield '</br>'
            name = function.__name__
            example = DOCS + '#' + name
            yield '<code><a href="%s">%s</a></code>' % (example, name)
        yield '</td>'

        yield '<td>'
        if meta.description:
            yield meta.description
            yield '</br>'
        if meta.tags:
            for tag in meta.tags:
                yield '#' + tag
            yield '</br>'
        for index, step in enumerate(meta.instruction):
            if index > 0:
                yield '</br>'
            yield step
        yield '</td>'

        yield '</tr>'
    yield '</table>'


def format_metas(metas):
    return '\n'.join(format_metas_(metas))


def show_html(html):
    from IPython.display import display, HTML

    display(HTML(html))


def patch_readme(html, path):
    text = load_text(path)
    text = re.sub(
        r'<!--- metas --->(.+)<!--- metas --->',
        '<!--- metas --->\n' + html + '\n<!--- metas --->',
        text,
        flags=re.S
    )
    dump_text(text, path)
