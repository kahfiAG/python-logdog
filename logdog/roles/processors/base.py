from __future__ import absolute_import, unicode_literals

import logging

from logdog.core.base_role import BaseRole


logger = logging.getLogger(__name__)


class BaseProcessor(BaseRole):

    def on_recv(self, data):
        self.output.send(data)