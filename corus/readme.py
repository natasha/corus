
import re

from .io import (
    load_text,
    dump_text
)


COMMANDS = ('wget', 'unzip', 'rm', 'tar')

KB = 1024
MB = 1024 * KB
GB = 1024 * MB


def is_command(step, commands=COMMANDS):
    return step.startswith(commands)


def format_bytes(value):
    value = value / MB
    if value < 1:
        return format(value, '.2f')
    else:
        return format_count(int(value))


def format_count(value):
    # https://stackoverflow.com/questions/16670125/python-format-string-thousand-separator-with-spaces/
    return format(value, ',').replace(',', ' ')


def format_metas_(metas, url):
    yield '<table>'
    yield '<tr>'
    yield '<th>Dataset</th>'
    yield '<th>API <code>from corus import</code></th>'
    yield '<th>Tags</th>'
    yield '<th>Records</th>'
    yield '<th>Uncompressed, Mb</th>'
    yield '<th>Description</th>'
    yield '</tr>'
    for meta in metas:
        yield '<tr>'

        yield '<td>'
        if meta.url:
            yield '<a href="%s">%s</a>' % (meta.url, meta.title)
        else:
            yield meta.title
        yield '</td>'

        yield '<td>'
        for index, function in enumerate(meta.functions):
            if index > 0:
                yield '</br>'
            name = function.__name__
            anchor = '#' + name
            if url:
                anchor = url + anchor
            yield '<code><a href="%s">%s</a></code>' % (anchor, name)
        yield '</td>'

        yield '<td>'
        if meta.tags:
            for tag in meta.tags:
                yield '#' + tag
        yield '</td>'

        yield '<td>'
        if meta.stats and meta.stats.count:
            yield format_count(meta.stats.count)
        yield '</td>'

        yield '<td>'
        if meta.stats and meta.stats.bytes:
            yield format_bytes(meta.stats.bytes)
        yield '</td>'

        yield '<td>'
        if meta.description:
            yield meta.description
            if meta.instruction:
                yield '</br>'
                yield '</br>'

        for index, step in enumerate(meta.instruction):
            if index > 0:
                yield '</br>'
            if is_command(step):
                yield '<code>%s</code>' % step
            else:
                yield step
        yield '</td>'

        yield '</tr>'
    yield '</table>'


def format_metas(metas, url=None):
    return '\n'.join(format_metas_(metas, url))


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
