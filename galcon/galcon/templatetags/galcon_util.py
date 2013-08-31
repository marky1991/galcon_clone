from django import template
from unidecode import unidecode
import re
from lxml.html.html5parser import document_fromstring
from bs4 import BeautifulSoup
from django.utils import timezone
from django.template import defaultfilters
from django.templatetags.static import static
from datetime import timedelta
from django.utils.safestring import mark_safe

from galcon.settings import STATIC_URL

from django.contrib.humanize.templatetags import humanize

import os

register = template.Library()
def me(context):
    return context["child"].author.user.username
commands = {"me": me}

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

@register.simple_tag
def get_full_url(child):
    url_pieces = []
    target = child
    url_pieces.append(target.to_url())
    while hasattr(target, "parent"):
        target = target.parent
        url_pieces.append(target.to_url())
    return "/".join(reversed(url_pieces))

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

@register.filter
def lookup(dictionary, key):
    return dictionary[key]

@register.filter
def to_flag(number):
    if number < 0:
        number = 0
    elif number > 9:
        number = 9
    
    return mark_safe("<img src='" + static("flags/{}.gif".format(number)) + "'/>")

@register.filter
def render_errors(field, is_all=False):
    out = []
    if not is_all: 
        for error in field.errors:
            out.append("<div class='error'>{}</div>".format(error))
    else:
        for error in field.errors["__all__"]:
            out.append("<div class='error'>{}</div>".format("\n".join(error.messages)))
    return mark_safe("/n".join(out))

@register.simple_tag
def highest_flag(name):
    from galcon.models import Player
    player = Player.objects.get(user__username=name)
    max_value = 0
    for attribute in filter(lambda att_name:
                            att_name.endswith("_rank"), dir(player)):
        val = getattr(player, attribute)
        if val > max_value:
            max_value = val
    return os.path.join([STATIC_URL, "flags", str(max_value), ".gif"])
