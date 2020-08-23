import re
import numpy as np
from pathlib import Path

# From https://github.com/fastai/fastai/blob/8dd982da14c9621418263d8fd431ff56bd2c533c/fastai/text/data.py
# To include special fastai tokens.
def apply_rules(text, pre_rules=[], post_rules=[]):
    "Apply `pre_rules` and `post_rules` to `text`"
    text = text.strip(' ')
    for r in pre_rules: text = r(text)
    toks = text.split()
    for r in post_rules: toks = r(toks)
    return ' '.join(toks)

# Modified from https://github.com/fastai/course-nlp/blob/master/nlputils.py
def split_wiki(file_path, destination, valid_pct=0.05, use_files_pct=1.0, lang='de', corpus_pre_rules=[], corpus_post_rules=[]):
    dest = Path(destination)
    train_dest = dest/'train'
    valid_dest = dest/'valid'
    corpus = dest/'corpus.txt'

    train_dest.mkdir(exist_ok=True, parents=True)
    valid_dest.mkdir(exist_ok=True, parents=True)

    title_re = re.compile(rf'<doc id="\d+" url="https://{lang}.wikipedia.org/wiki\?curid=\d+" title="([^"]+)">')
    f = None
    skip_file = False

    np.random.seed(420)
    lines = Path(file_path).open()
    with open(corpus, 'w') as corpus_file:
        for i,l in enumerate(lines):
            if i%1000000 == 0: print(i)
            if l.startswith('<doc id="'):
                if np.random.uniform() > use_files_pct:
                    skip_file = True
                    continue
                else:
                    skip_file = False
                title = title_re.findall(l)[0].replace('/','_')
                if f: f.close()
                if np.random.uniform() > valid_pct:
                    f = (train_dest/f'{title}.txt').open('w')
                else:
                    f = (valid_dest/f'{title}.txt').open('w')
            elif not skip_file:
                l = apply_rules(l) + '\n'
                f.write(l.replace('</doc>', ''))
                corpus_file.write(l)
        f.close()
    return dest