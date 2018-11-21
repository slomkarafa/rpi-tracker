class Rider:
    def __init__(self, left_motor, right_motor):
        self.l_m = left_motor
        self.r_m = right_motor
        self.speed = 0
        self.ratio = 1

    def ride(self, left, right):
        self.l_m.run(left)
        self.r_m.run(right)

    def stop(self, kind='SOFT'):
        for m in (self.l_m, self.r_m):
            m.set_speed(0 if kind == 'SOFT' else 100)
            m.set_direction('STOP')
