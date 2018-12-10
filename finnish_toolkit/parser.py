import traceback
import pdb
import os
import sys
import time
import collections

if __name__ == "__main__":
    if sys.path[0] != '':
        sys.path.insert(0, '')

sys.path.append(os.getcwd() + '/finnish_parser')
try:
    from finnish_parser.full_pipeline_stream import read_pipelines
    from finnish_parser.pipeline import Pipeline
except:
    raise


class Parser:
    def __init__(self,
                 conf_yaml='./models_fi_tdt/pipelines.yaml',
                 selected_pipeline='parse_plaintext'):
        if not conf_yaml:
            raise ValueError('conf yaml for the pipelines are needed.')
        if not os.path.exists(conf_yaml):
            raise FileNotFoundError('conf yaml not found!')

        self.conf_yaml = conf_yaml
        self.selected_pipeline = selected_pipeline
        self.pipelines = read_pipelines(conf_yaml)
        self.pipeline = Pipeline(steps=self.pipelines[selected_pipeline])

    def parse(self, text):
        pipeline = self.pipeline

        job_id = pipeline.put(text)
        while pipeline.is_alive():
            res = pipeline.get(job_id)
            if res is None:
                time.sleep(0.1)
            else:
                break
        return res

# Visualization


def _read_conll(conll_text):
    if not conll_text:
        raise ValueError('Visualization conll_text is none.')

    lines = conll_text.split('\n')
    sent = []
    comments = []
    for line in lines:
        line = line.strip()
        if not line:
            if sent:
                yield sent, comments
                sent = []
                comments = []
        elif line.startswith(u"#"):
            if sent:
                raise ValueError("Missing newline after sentence")
            comments.append(line)
            continue
        else:
            sent.append(line.split(u"\t"))
    else:
        if sent:
            yield sent, comments


def _sort_feat(f):
    # CoNLL-U requirement -> turn off when no longer required by the visualizer
    if f == u"_":
        return f
    new_list = []
    for attr_val in f.split(u"|"):
        if u"=" in attr_val:
            attr, val = attr_val.split(u"=", 1)
        else:
            attr, val = attr_val.split(u"_", 1)
        attr = attr.capitalize()
        val = val.capitalize()
        val = val.replace(u"_", u"")
        new_list.append(attr+u"="+val)
    return u"|".join(sorted(new_list))


def _d(cols, idx):
    if idx is None:
        return u"_"
    else:
        return cols[idx]


def visualize(conll_text,
              output_path,
              template_path='./finnish_toolkit/templates/vis_template.html'):
    if not conll_text:
        raise ValueError('Input text is missing.')
    if not output_path:
        raise ValueError('Output path is missing.')
    if not os.path.isfile(template_path):
        raise FileNotFoundError('Template file not found.')

    header = u'<div class="conllu-parse">\n'
    footer = u'</div>\n'

    Format = collections.namedtuple('Format',
                                    [
                                        'ID',
                                        'FORM',
                                        'LEMMA',
                                        'CPOS',
                                        'POS',
                                        'FEAT',
                                        'HEAD',
                                        'DEPREL',
                                        'DEPS',
                                        'MISC'
                                    ])
    f_09 = Format(0, 1, 2, 4, 4, 6, 8, 10, None, None)
    f_u = Format(0, 1, 2, 3, 4, 5, 6, 7, 8, 9)

    #         0  1    2     3       4  5    6    7      8    9     10     11
    # conll-u  ID FORM LEMMA CPOS   POS FEAT HEAD DEPREL DEPS MISC
    # conll-09 ID FORM LEMMA PLEMMA POS PPOS FEAT PFEAT  HEAD PHEAD DEPREL PDEPREL _ _

    data_to_print = u""
    for sent, comments in _read_conll(conll_text):
        tree = header
        if comments:
            tree += u"\n".join(comments)+u"\n"
        for line in sent:
            if len(line) == 10:  # conll-u
                f = f_u
            else:
                f = f_09
            line[f.FEAT] = _sort_feat(line[f.FEAT])
            # take idx,token,lemma,pos,pos,feat,deprel,head
            l = u"\t".join(_d(line, idx) for idx in [f.ID,
                                                     f.FORM,
                                                     f.LEMMA,
                                                     f.CPOS,
                                                     f.POS,
                                                     f.FEAT,
                                                     f.HEAD,
                                                     f.DEPREL,
                                                     f.DEPS,
                                                     f.MISC])
            tree += l+u"\n"
        tree += u"\n"  # conll-u expects an empty line at the end of every tree
        tree += footer
        data_to_print += tree
    with open(template_path) as template:
        data = template.read().replace(u"CONTENTGOESHERE", data_to_print, 1)
        with open(output_path, 'w') as output_file:
            output_file.write(data)


if __name__ == "__main__":
    # parse
    mp = Parser('./models_fi_tdt/pipelines.yaml',
                'parse_plaintext')
    res = mp.parse(
        'Jos tavoitteenasi on seurustelusuhde, \
        kannustamme panostamaan auton ohella myös \
        ihmissuhdetaitoihin.')

    # visualize
    if not os.path.exists('./temp'):
        os.mkdir('./temp')
    visualize(res, './temp/output.html')
