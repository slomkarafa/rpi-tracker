from datetime import datetime
from functools import reduce
from pathlib import Path

from aiofile import AIOFile


class Saver:
    def __init__(self, file, path):
        self.file = file
        self.path = path

    @classmethod
    async def create(cls, main_path, name=None, header=None):
        save_path = f'{main_path}/{name or str(datetime.now().strftime("%d:%m:%Y_%H:%M:%S"))}'
        Path(save_path).mkdir(exist_ok=True, parents=True)
        file = await AIOFile(f'{save_path}/imu_enc.csv', 'a')
        if header:
            await file.write(header)
        return cls(file, save_path)

    async def add(self, *args):

        string = reduce(lambda prev, x: prev+';'+str(x), args[1:], str(args[0])) + '\n'
        await self.file.write(string)


    async def finish(self):
        await self.file.close()

    async def add_description(self, text):
        async with AIOFile(f'{self.path}/info.csv', 'w') as file:
            await file.write(text)
