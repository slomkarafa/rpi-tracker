from datetime import datetime
from pathlib import Path


class Saver:
    def __init__(self, save_path, name=None):
        Path(save_path).mkdir(exist_ok=True, parents=True)
        self.name = name or str(datetime.now().strftime("%d:%m:%Y_%H:%M:%S.csv"))
        self.file = open(f'{save_path}/{self.name}', 'a')

    def add(self, *args):
        self.file.write(f'{",".join(args)}\n')

    def finish(self):
        self.file.close()

    def __del__(self):
        if not self.file.closed:
            self.finish()
