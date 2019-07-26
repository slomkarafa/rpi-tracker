from datetime import datetime


class Saver:
    def __init__(self, save_path, name=None):
        self.name = name or str(datetime.now().strftime("%d:%m:%Y_%H:%M:%S.csv"))
        self.file = open(f'{save_path}/{self.name}', 'a')

    def add(self, slam, gyro, acc, mgn):
        self.file.write(f'{slam};{gyro};{acc};{mgn}\n')

    def __del__(self):
        self.file.close()
