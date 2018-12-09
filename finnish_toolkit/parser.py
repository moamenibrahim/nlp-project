import traceback
import pdb
import os
import sys
import time
import multiprocessing

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
        while True:
            res = pipeline.get(job_id)
            if res is None:
                time.sleep(0.1)
            else:
                break
        return res


if __name__ == "__main__":
    mp = Parser('./models_fi_tdt/pipelines.yaml',
                'parse_plaintext')
    res = mp.parse(
        'Jos tavoitteenasi on seurustelusuhde, \
        kannustamme panostamaan auton ohella myös \
        ihmissuhdetaitoihin.')
    print(res)
