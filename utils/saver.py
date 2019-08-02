from datetime import datetime

class Saver:
    def __init__(self, save_path, name=None):
        self.name = name or str(datetime.now().strftime("%d:%m:%Y_%H:%M:%S.csv"))
        self.file = open(f'{save_path}/{self.name}', 'a')

    def add(self, *args):
        self.file.write(f'{",".join(args)}\n')

    def finish(self):
        self.file.close()

    def __del__(self):
        self.finish()


# def gather_data(saver):
#     async def collector()

# class SaverHandler:
#     def __init__(self):
#         self.saver = None
#         self.collector = None
#
#     def start(self, loop):
#         if not self.saver:
#             self.collector = loop.run_until_complete(gather_data(saver))