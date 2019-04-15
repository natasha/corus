
import re

from .io import (
    load_text,
    dump_text
)


DOCS = 'https://nbviewer.jupyter.org/github/natasha/corus/blob/master/docs.ipynb'


def format_registry_(registry):
    yield '<table>'
    yield '<tr>'
    yield '<th>Dataset</th>'
    yield '<th>API <code>from corus import</code></th>'
    yield '<th>Usage</th>'
    yield '</tr>'
    for meta, function in registry:
        example = DOCS + '#' + meta.label
        function = 'load_' + meta.label

        yield '<tr>'

        yield '<td>'
        yield '<a href="%s">%s</a>' % (meta.source, meta.title)
        yield '</td>'

        yield '<td>'
        yield '<code>%s</code>' % function
        yield '</td>'

        yield '<td>'
        for step in meta.instruction:
            yield step
            yield '</br>'
        yield 'See <code>%s</code> <a href="%s">usage example</a>' % (function, example)
        yield '</td>'

        yield '</tr>'
    yield '</table>'


def format_registry(registry):
    return '\n'.join(format_registry_(registry))


def show_html(html):
    from IPython.display import display, HTML

    display(HTML(html))


def patch_readme(html, path):
    text = load_text(path)
    text = re.sub(
        r'<!--- registry --->(.+)<!--- registry --->',
        '<!--- registry --->\n' + html + '\n<!--- registry --->',
        text,
        flags=re.S
    )
    dump_text(text, path)
