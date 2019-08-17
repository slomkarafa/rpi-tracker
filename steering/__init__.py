from utils.helpers import should_use

if should_use('GPIO'):
    from steering.rider.rider import Rider
else:
    from steering.rider.rider_unplugged import UnpluggedRider as Rider
