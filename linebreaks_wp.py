import re
from django import template
from django.utils.functional import allow_lazy
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe, SafeData
from django.utils.encoding import force_unicode
from django.utils.html import escape
from django.utils.text import normalize_newlines
register = template.Library()

def linebreaks_wp(pee, autoescape=False):
    """Straight up port of http://codex.wordpress.org/Function_Reference/wpautop"""
    if (pee.strip() == ""):
        return ""
    pee = normalize_newlines(pee)
    pee = pee + "\n"
    pee = re.sub(r'<br />\s*<br />', "\n\n", pee)
    allblocks = r'(?:table|thead|tfoot|caption|col|colgroup|tbody|tr|td|th|div|dl|dd|dt|ul|ol|li|pre|select|option|form|map|area|blockquote|address|math|style|input|p|h[1-6]|hr|fieldset|legend|section|article|aside|hgroup|header|footer|nav|figure|figcaption|details|menu|summary)'
    pee = re.sub(r'(<' + allblocks + '[^>]*>)', lambda m: "\n"+m.group(1) if m.group(1) else "\n", pee)
    pee = re.sub(r'(</' + allblocks + '>)', lambda m: m.group(1)+"\n\n" if m.group(1) else "\n\n", pee)
    #pee = pee.replace("\r\n", "\n")
    #pee = pee.replace("\r", "\n") #these taken care of by normalize_newlines
    if (pee.find("<object") != -1):
        pee = re.sub(r'\s*<param([^>]*)>\s*', lambda m: "<param%s>" % (m.group(1) if m.group(1) else "", ), pee) # no pee inside object/embed
        pee = re.sub(r'\s*</embed>\s*', '</embed>', pee)
    pee = re.sub(r"\n\n+", "\n\n", pee) # take care of duplicates
    pees = re.split(r'\n\s*\n', pee) # since PHP has a PREG_SPLIT_NO_EMPTY, may need to go through and drop any empty strings
    #pees = [p for p in pees if p]
    pee = "".join(["<p>%s</p>\n" % tinkle.strip('\n') for tinkle in pees])
    pee = re.sub(r'<p>\s*</p>', '', pee) #under certain strange conditions it could create a P of entirely whitespace
    pee = re.sub(r'<p>([^<]+)</(div|address|form)>', lambda m: "<p>%s</p></%s>" % ((lambda x: x.group(1) if x.group(1) else "")(m), (lambda x: x.group(2) if x.group(2) else "")(m), ), pee)
    pee = re.sub(r'<p>\s*(</?' + allblocks + r'[^>]*>)\s*</p>', lambda m: m.group(1) if m.group(1) else "", pee) # don't pee all over a tag
    pee = re.sub(r"<p>(<li.+?)</p>", lambda m: m.group(1) if m.group(1) else "", pee) # problem with nested lists
    pee = re.sub(r'<p><blockquote([^>]*)>', lambda m: "<blockquote%s><p>" % (m.group(1) if m.group(1) else "",), pee, flags=re.IGNORECASE)
    pee = pee.replace('</blockquote></p>', '</p></blockquote>')
    pee = re.sub(r'<p>\s*(</?' + allblocks + r'[^>]*>)', lambda m: m.group(1) if m.group(1) else "", pee)
    pee = re.sub(r'(</?' + allblocks + '[^>]*>)\s*</p>', lambda m: m.group(1) if m.group(1) else "", pee)

    def _autop_newline_preservation_helper(matches):
        return matches.group(0).replace("\n", "<WPPreserveNewline />")
    pee = re.sub(r'<(script|style).*?</\1>', _autop_newline_preservation_helper, pee, flags=re.DOTALL)
    pee = re.sub(r'(?<!<br />)\s*\n', "<br />\n", pee) # make line breaks
    pee = pee.replace('<WPPreserveNewline />', "\n")

    pee = re.sub(r'(</?' + allblocks + '[^>]*>)\s*<br />', lambda m: m.group(1) if m.group(1) else "", pee)
    pee = re.sub(r'<br />(\s*</?(?:p|li|div|dl|dd|dt|th|pre|td|ul|ol)[^>]*>)', lambda m: m.group(1) if m.group(1) else "", pee)
    if (pee.find('<pre') != -1):
        def clean_pre(m):
            if m.group(1) and m.group(2):
                text = m.group(2)
                text = text.replace('<br />', '')
                text = text.replace('<p>', "\n")
                text = text.replace('</p>', '')
                text = m.group(1)+escape(text)+"</pre>"
            else:
                text = m.group(0)
                text = text.replace('<br />', '')
                text = text.replace('<p>', "\n")
                text = text.replace('</p>', '')

            return text
        pee = re.sub('(?is)(<pre[^>]*>)(.*?)</pre>', clean_pre, pee)
    pee = re.sub( r"\n</p>$", '</p>', pee)
    return pee
linebreaks_wp = allow_lazy(linebreaks_wp, unicode)

@register.filter("linebreaks_wp")
@stringfilter
def linebreaks_wp_filter(value, autoescape=None):
    """Straight up port of http://codex.wordpress.org/Function_Reference/wpautop"""
    autoescape = autoescape and not isinstance(value, SafeData)
    return mark_safe(linebreaks_wp(value, autoescape))
linebreaks_wp_filter.is_safe = True
linebreaks_wp_filter.needs_autoescape = True
linebreaks_wp = stringfilter(linebreaks_wp)
