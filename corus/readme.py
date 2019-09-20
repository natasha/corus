
from __future__ import division

import re

from .sources.meta import is_group
from .io import (
    load_text,
    dump_text
)


COMMANDS = ('wget', 'unzip', 'rm', 'tar')

KB = 1024
MB = 1024 * KB
GB = 1024 * MB

LABELS = {
    KB: 'Kb',
    MB: 'Mb',
    GB: 'Gb'
}


def is_command(step, commands=COMMANDS):
    return step.startswith(commands)


def format_bytes(value):
    value /= KB
    unit = KB
    for _ in range(2):
        if value < KB:
            break
        value /= KB
        unit *= KB
    return '%.2f %s' % (value, LABELS[unit])


def format_count(value):
    # https://stackoverflow.com/questions/16670125/python-format-string-thousand-separator-with-spaces/
    return format(value, ',').replace(',', '&nbsp;')


def unfold_metas(items):
    for item in items:
        if is_group(item):
            yield True, item
            for meta in item.metas:
                yield False, meta
        else:
            yield False, item


def format_metas_(metas, url):
    yield '<table>'
    yield '<tr>'
    yield '<th>Dataset</th>'
    yield '<th>API <code>from corus import</code></th>'
    yield '<th>Tags</th>'
    yield '<th>Texts</th>'
    yield '<th>Uncompressed</th>'
    yield '<th>Description</th>'
    yield '</tr>'
    for group, meta in unfold_metas(metas):
        yield '<tr>'

        yield '<td>'
        if meta.url:
            yield '<a href="%s">%s</a>' % (meta.url, meta.title)
        else:
            yield meta.title
        yield '</td>'

        if not group:
            yield '<td>'
            for index, function in enumerate(meta.functions):
                if index > 0:
                    yield '</br>'
                name = function.__name__
                # to refer to cells in readme table
                yield '<a name="%s"></a>' % name
                anchor = '#' + name
                if url:
                    anchor = url + anchor
                yield '<code><a href="%s">%s</a></code>' % (anchor, name)
            yield '</td>'

            yield '<td>'
            if meta.tags:
                for tag in meta.tags:
                    yield '<code>%s</code>' % tag
            yield '</td>'

            yield '<td align="right">'
            if meta.stats and meta.stats.count:
                yield format_count(meta.stats.count)
            yield '</td>'

            yield '<td align="right">'
            if meta.stats and meta.stats.bytes:
                yield format_bytes(meta.stats.bytes)
            yield '</td>'

        if group:
            yield '<td colspan="5">'
        else:
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
