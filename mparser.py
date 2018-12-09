import os
import time
import sys
import multiprocessing

sys.path.append(os.getcwd()+'/finnish_parser')

from finnish_parser.full_pipeline_stream import read_pipelines
from finnish_parser.pipeline import Pipeline

class Parser:

    def __init__(self, conf_yaml, pipeline):
        if not conf_yaml:
            conf_yaml = os.getcwd() + "/finnish_parser/models_fi_tdt/pipelines.yaml"

        if not os.path.exists(conf_yaml):
            raise FileNotFoundError()

        if not pipeline:
            pipeline = 'parse_plaintext'

        self.conf_yaml = conf_yaml
        self.pipeline = pipeline
        self.pipelines = read_pipelines(conf_yaml)
        self.p = Pipeline(steps=self.pipelines[pipeline])

    def parse(self, txt):
        p = self.p

        job_id = p.put(txt)
        while True:
            res = p.get(job_id)
            if res is None:
                time.sleep(0.1)
            else:
                break
        return res


if __name__ == "__main__":
    multiprocessing.set_start_method('fork', force=True)
    mp = Parser('./finnish_parser/models_fi_tdt/pipelines.yaml', 'parse_plaintext')
    res = mp.parse('Jos tavoitteenasi on seurustelusuhde, kannustamme panostamaan auton ohella myös ihmissuhdetaitoihin.')

    print(res)
