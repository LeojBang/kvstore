import time
from collections import OrderedDict
import threading


class InMemoryStore:

    def __init__(self):
        self._lock = threading.Lock()
        self._data = OrderedDict()

    def _is_expired(self, expires_at):
        return expires_at is not None and time.time() > expires_at

    def put(self, key, value, ttl_seconds=0):
        with self._lock:
            if ttl_seconds > 0:
                expires_at = time.time() + ttl_seconds
            else:
                expires_at = None
            if key not in self._data and len(self._data) >= 10:
                self._data.popitem(last=False)
            self._data[key] = value, expires_at
            self._data.move_to_end(key)

    def get(self, key):
        with self._lock:
            if key not in self._data:
                return None
            value, expires_at = self._data[key]
            if self._is_expired(expires_at):
                del self._data[key]
                return None
            self._data.move_to_end(key)
            return value

    def delete(self, key):
        with self._lock:
            self._data.pop(key, None)

    def list(self, prefix):
        with self._lock:
            items = []
            for key, value in self._data.items():
                val, expires_at = value
                if self._is_expired(expires_at):
                    del self._data[key]
                    continue
                if key.startswith(prefix):
                    items.append((key, val))
            return items
