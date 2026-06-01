"""Stdlib logging config with a tqdm-friendly handler."""
from __future__ import annotations

import logging
import sys


class _TqdmHandler(logging.StreamHandler):
    def emit(self, record):
        try:
            from tqdm import tqdm
            msg = self.format(record)
            tqdm.write(msg, file=self.stream)
            self.flush()
        except ImportError:
            super().emit(record)


_configured = False


def get_logger(name: str = "propaganda_lt", level: int = logging.INFO) -> logging.Logger:
    global _configured
    logger = logging.getLogger(name)
    if not _configured:
        logger.setLevel(level)
        h = _TqdmHandler(sys.stderr)
        h.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                                         "%H:%M:%S"))
        logger.addHandler(h)
        logger.propagate = False
        _configured = True
    return logger
