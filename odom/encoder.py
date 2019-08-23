import apigpio


class Encoder:
    def __init__(self, pi, dir_0, dir_1):
        self.dir0_pin = dir_0
        self.dir1_pin = dir_1
        self.pi = pi
        self.state = {dir_0: 0, dir_1: 0}
        self.count = 0

    def reset(self):
        self.count = 0

    def on_rise(self, gpio, level, _):
        self.state[gpio] = level
        if self.state[self.dir0_pin] and not self.state[self.dir1_pin]:
            self.count += -1 if level else 1
        elif not self.state[self.dir0_pin] and self.state[self.dir1_pin]:
            self.count += 1 if level else -1


    @classmethod
    async def create(cls, pi, config):
        dir_0, dir_1 = config['dir_0'], config['dir_1']
        await pi.set_mode(dir_0, apigpio.INPUT)
        await pi.set_mode(dir_1, apigpio.INPUT)
        enc = cls(pi, dir_0, dir_1)
        await enc.pi.add_callback(dir_0, edge=apigpio.EITHER_EDGE, func=enc.on_rise)
        await enc.pi.add_callback(dir_1, edge=apigpio.EITHER_EDGE, func=enc.on_rise)
        return enc
