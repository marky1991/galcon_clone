from lxml.html import clean
from bs4 import BeautifulSoup
from itertools import takewhile

allowed_tags = ["a", "abbr", "address", "area", "article", "aside",
                "audio","span", "div"]

allowed_tags = allowed_tags + ["raw"]

cleaner = clean.Cleaner(allow_tags=allowed_tags, remove_unknown_tags = False)

class Forum_Spot:
    levels = ["forum", "section", "subsection", "thread", "post"]
    def __init__(self, url):
        parts = url.strip("/").split("/")
        self.level = Forum_Spot.levels[len(parts)-1]
        parts = parts + [None]*(5 - len(parts))
        self.root, self.section, self.subsection, self.thread, self.post = parts
    def __iter__(self):
        return zip(Forum_Spot.levels, takewhile(lambda x: x is not None, [self.root, self.section, self.subsection,
                                       self.thread, self.post]))
                                       

def clean_post(post):
    """Cleans a post, removing banned tags. Note: Assumes html5."""
    post = cleaner.clean_html(post)
    post = BeautifulSoup(post)
    for audio_tag in post.find_all("audio"):
        audio_tag["autoplay"] = False
    return str(post)
