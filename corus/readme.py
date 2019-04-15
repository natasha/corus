
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
    yield '<th>How to download</th>'
    yield '</tr>'
    for meta, function in registry:
        example = DOCS + '#' + meta.label
        function = 'load_' + meta.label

        yield '<tr>'

        yield '<td>'
        yield '<a href="%s">%s</a>' % (meta.source, meta.title)
        yield '</br>'
        yield meta.description
        yield '</td>'

        yield '<td>'
        yield '<code>%s</code>' % function
        yield '</br>'
        yield '<a href="%s">usage example</a>' % example
        yield '</td>'

        yield '<td>'
        for index, step in enumerate(meta.instruction):
            if index > 0:
                yield '</br>'
            yield step
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
