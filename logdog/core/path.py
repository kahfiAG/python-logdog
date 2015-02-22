import logging
import os


logger = logging.getLogger(__name__)


class Path(object):
    __slots__ = ('name', 'stat', '_prev_stat', 'offset', '_f', '_last_read_line')

    def __init__(self, name, offset, stat):
        self.name = name
        self.stat = self._prev_stat = stat
        self.offset = offset

        self._f = self._last_read_line = None

    def open(self):
        self._f = open(self.name, 'r')
        self._f.seek(self.offset)
        self._prev_stat = self.stat
        self.stat = os.stat(self.name)

    def close(self):
        self._f.close()

    def reopen(self):
        self.close()
        self.open()

    def check_stat(self):
        """Is called if we have nothing to read"""
        self._prev_stat = self.stat
        self.stat = os.stat(self.name)

        if not self.is_same_file(self._prev_stat, self.stat):
            logger.debug('[FILE:%s] New file detected by this path. Re-opening...', self.name)
            self.offset = 0
            self.reopen()

        elif self.is_file_truncated(self._prev_stat, self.stat):
            logger.debug('[FILE:%s] Seems, file was truncated. Re-opening...', self.name)
            self.offset = 0
            self.reopen()

    @staticmethod
    def is_same_file(prev_stat, cur_stat):
        return prev_stat.st_ino == cur_stat.st_ino and prev_stat.st_dev and cur_stat.st_dev

    @staticmethod
    def is_file_truncated(prev_stat, cur_stat):
        return prev_stat.st_size > cur_stat.st_size

    def read_line(self):
        self._last_read_line = (_, line) = (self.offset, self._f.readline())
        self.offset = self._f.tell()
        return line
