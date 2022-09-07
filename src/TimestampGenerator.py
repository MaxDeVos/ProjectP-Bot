import time


def get_time_stamp(stamp):
    return f"[{stamp}] [{time.strftime('%Y-%m-%d %H:%M:%S')}]"


class TimestampGenerator:
    def __init__(self, stamp):
        self.stamp = stamp

    def get_time_stamp(self):
        return f"[{self.stamp}] [{time.strftime('%Y-%m-%d %H:%M:%S')}]"
