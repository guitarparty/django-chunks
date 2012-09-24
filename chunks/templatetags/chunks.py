from django import template
from django.db import models
from django.core.cache import cache
from django.contrib.markup.templatetags.markup import markdown

register = template.Library()

Chunk = models.get_model('chunks', 'chunk')
CACHE_PREFIX = "chunk_"

def do_chunk(parser, token):
    # split_contents() knows not to split quoted strings.
    tokens = token.split_contents()
    if len(tokens) < 2 or len(tokens) > 3:
        raise template.TemplateSyntaxError, "%r tag should have either 2 or 3 arguments" % (tokens[0],)
    if len(tokens) == 2:
        tag_name, key = tokens
        cache_time = 0
    if len(tokens) == 3:
        tag_name, key, cache_time = tokens
    key = ensure_quoted_string(key, "%r tag's argument should be in quotes" % tag_name)
    return ChunkNode(key, cache_time)

class ChunkNode(template.Node):
    def __init__(self, key, cache_time=0):
       self.key = key
       self.cache_time = int(cache_time)
       self.lang_code = template.Variable('LANGUAGE_CODE')

    def render(self, context):
        try:
            lang = self.lang_code.resolve(context)
        except template.VariableDoesNotExist:
            # no LANGUAGE_CODE variable found in context, just return ''
            return ''
        cache_key = CACHE_PREFIX + self.key + lang
        content = cache.get(cache_key)
        if content is None:
            try:
                chunk = Chunk.objects.get(key=self.key, lang_code=lang)
                content = chunk.content
            except Chunk.DoesNotExist:
                # cache missing models as empty chunk strings
                content = ''
            if self.cache_time > 0: 
                # don't even call cache if timeout is 0
                cache.set(cache_key, content, self.cache_time)
        return markdown(content)


def do_get_chunk(parser, token):
    tokens = token.split_contents()
    if len(tokens) != 4 or tokens[2] != 'as':
        raise template.TemplateSyntaxError, 'Invalid syntax. Usage: {%% %s "key" as varname %%}' % tokens[0]
    tagname, key, varname = tokens[0], tokens[1], tokens[3]
    key = ensure_quoted_string(key, "Key argument to %r must be in quotes" % tagname)
    return GetChunkNode(key, varname)

class GetChunkNode(template.Node):
    def __init__(self, key, varname):
        self.key = key
        self.varname = varname

    def render(self, context):
        try:
            chunk = Chunk.objects.get(key=self.key)
        except Chunk.DoesNotExist:
            chunk = None
        context[self.varname] = chunk
        return ''


def ensure_quoted_string(string, error_message):
    '''
    Check to see if the key is properly double/single quoted and
    returns the string without quotes
    '''
    if not (string[0] == string[-1] and string[0] in ('"', "'")):
        raise template.TemplateSyntaxError, error_message
    return string[1:-1]


register.tag('chunk', do_chunk)
register.tag('get_chunk', do_get_chunk)
