from datetime import datetime
from functools import reduce
from pathlib import Path

from aiofile import AIOFile


class Saver:
    def __init__(self, file):
        self.file = file

    @classmethod
    async def create(cls, save_path, name=None, header=None):
        Path(save_path).mkdir(exist_ok=True, parents=True)
        name = name or str(datetime.now().strftime("%d:%m:%Y_%H:%M:%S.csv"))
        file = await AIOFile(f'{save_path}/{name}', 'a')
        if header:
            await file.write(header)
        return cls(file)

    async def add(self, *args):
        print(args)
        # await self.file.write()

        string = reduce(lambda prev, x: prev+','+str(x), args[1:], str(args[0])) + '\n'
        # for x in args:
        #     print(type(x))
        await self.file.write(string)

        print('saved')

    async def finish(self):
        await self.file.close()

    # def __del__(self):
    #     if not self.file.cself.finish()losed:
    #
