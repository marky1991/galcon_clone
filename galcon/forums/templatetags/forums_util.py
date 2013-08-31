from unidecode import unidecode
import re
from lxml.html import clean
from lxml.html.html5parser import document_fromstring
from bs4 import BeautifulSoup
from datetime import timedelta

from django import template
from django.utils import timezone
from django.template import defaultfilters
from django.templatetags.static import static
from django.utils.safestring import mark_safe
from django.contrib.humanize.templatetags import humanize

register = template.Library()
def me(context):
    return context["child"].author.user.username
commands = {"me": me}
allowed_tags = ["a", "abbr", "address", "area", "article", "aside",
                "audio",
                            "span", "div"]

allowed_tags = allowed_tags + ["raw"]
cleaner = clean.Cleaner(allow_tags=allowed_tags, remove_unknown_tags = False)


@register.filter
def make_url(txt):
    """A custom version of slugify that retains non-ascii characters. The purpose of this
    function in the application is to make URLs more readable in a browser, so there are 
    some added heuristics to retain as much of the title meaning as possible while 
    excluding characters that are troublesome to read in URLs. For example, question marks 
    will be seen in the browser URL as %3F and are thereful unreadable. Although non-ascii
    characters will also be hex-encoded in the raw URL, most browsers will display them
    as human-readable glyphs in the address bar -- those should be kept in the slug."""
    txt = txt.strip() # remove trailing whitespace
    txt = unidecode(txt).lower()
    txt = re.sub('\s*-\s*','-', txt, re.UNICODE) # remove spaces before and after dashes
    txt = re.sub('[\s/]', '_', txt, re.UNICODE) # replace remaining spaces with underscores
    txt = re.sub('(\d):(\d)', r'\1-\2', txt, re.UNICODE) # replace colons between numbers with dashes
    txt = re.sub('"', "'", txt, re.UNICODE) # replace double quotes with single quotes
    txt = re.sub(r'[?,:!@#~`+=$%^&\\*()\[\]{}<>]','',txt, re.UNICODE) # remove some characters altogether
    return txt

@register.filter
def plaintext(txt):
    txt = txt.strip()
    txt = unidecode(txt)
    soup = BeautifulSoup(txt)
    return "".join(soup.find_all(text=True))

@register.simple_tag(takes_context=True)
def child_link(context):
    child = context["child"]
    request = context["request"]
    return '<a href="' + request.path + make_url(child.to_url()) + '/">' + child.title + '</a>'


@register.simple_tag(takes_context=True)
def latest_post_info(context, level):
    from ..models import Post
    session = context["request"].session
    child = context["child"]
    if level == "section":
        kwargs = {"parent__parent__parent__pk": child.pk}
    elif level == "subsection":
        kwargs = {"parent__parent__pk": child.pk}
    elif level == "thread":
        kwargs = {"parent__pk": child.pk}
    else:
        raise TypeError("Invalid child type: {}".format(child))
    latest_post = Post.objects.filter(hidden=False, **kwargs).latest()
    return "<br/>".join(["<a href='/forums/"  + latest_post.full_url + "/'>" +
                         latest_post.title + "</a>", str(latest_post.author),
                         format_time(timezone.localtime(latest_post.last_modification_date))])

@register.filter(expects_localtime=True)
def format_date(time):
    #This happens for the anonymous user
    if time == "":
        return ""
    one_day = timedelta(1)
    now = timezone.now()
    if abs(time - now) > one_day:
        return time.date()
    else:
        return humanize.naturaltime(time)


@register.filter(expects_localtime=True)
def format_time(time):
    return time.strftime("%b {0}, %Y @ {1}:%m %p").format(time.day, time.hour % 12).replace("AM", "a.m.").replace("PM", "p.m.")

@register.simple_tag(takes_context=True)
def render_post(context, post):
    post = BeautifulSoup(post)
    lines = []
    #Naively, this is O(n^3) behavior. For all realistic inputs, it's O(n) because the number of commands and escaped slashes
    #is basically O(1). In the worst (typical) case, it's O(n^2). This case will not come up unless the user makes a post of only
    #escaped slashes. Even if he does this, n will be fairly small, so this is acceptable.

    new_lines = []
    for line in reversed(post.find_all(text=True)):
        #print("Type:", type(line), dir(line))
        words = line.split("\/")
        new_words = []
        for word in words:
            for command in commands:
                word = word.replace("/"+command, commands[command](context))
            new_words.append(word)
        #print("New line: ", "\/".join(new_words))
        line.replace_with("/".join(new_words).replace("THE LORD", "<span style='color: #FF0000'>THE LORD</span>"))
    context["post"] = str(post.body.next)
    #print("Dir(post), post.strings: ", dir(post), list(post.strings))
    #print("POst: ", str(post))
    return ""

@register.filter
def lookup(dictionary, key):
    return dictionary[key]

@register.filter
def get_attr(obj, attribute):
    return getattr(obj, attribute)

@register.filter
def to_flag(number):
    if number < 0:
        number = 0
    elif number > 9:
        number = 9
    
    return mark_safe("<img src='" + static("flags/{}.gif".format(number)) + "'/>")

@register.filter
def render_errors(field):
    out = []
    for error in field.errors:
        out.append("<div class='error'>{}</div>".format(error))
    return mark_safe("/n".join(out))
