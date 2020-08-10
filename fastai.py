from fastai.text import *

# From https://github.com/fastai/fastai/blob/8dd982da14c9621418263d8fd431ff56bd2c533c/fastai/text/data.py
# To include special fastai tokens.
def apply_rules(text, pre_rules=None, post_rules=None):
    "Apply `pre_rules` and `post_rules` to `text`"
    text = text.strip(' ')
    for r in ifnone(pre_rules, defaults.text_pre_rules): text = r(text)
    toks = text.split()
    for r in ifnone(post_rules, defaults.text_post_rules): toks = r(toks)
    return ' '.join(toks)