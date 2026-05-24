import json
import logging
import redis as redis_lib

logger = logging.getLogger(__name__)

# FIXME: вынести в env переменные
_REDIS_HOST = "localhost"
_REDIS_PORT = 6379
_REDIS_DB = 0
DEFAULT_TTL = 60  # секунд

_r: redis_lib.Redis | None = None

try:
    _r = redis_lib.Redis(host=_REDIS_HOST, port=_REDIS_PORT, db=_REDIS_DB, decode_responses=True)
    _r.ping()
    logger.info("Redis connected")
except Exception as e:
    logger.warning(f"Redis unavailable, caching disabled: {e}")
    _r = None


def get(key: str):
    if not _r:
        return None
    try:
        val = _r.get(key)
        return json.loads(val) if val else None
    except Exception:
        return None


def set(key: str, data, ttl: int = DEFAULT_TTL):
    if not _r:
        return
    try:
        _r.setex(key, ttl, json.dumps(data, ensure_ascii=False, default=str))
    except Exception:
        pass


def invalidate(pattern: str):
    """Удаляет все ключи по паттерну. scan_iter безопаснее flushdb для продакшена."""
    if not _r:
        return
    try:
        keys = list(_r.scan_iter(pattern))
        if keys:
            _r.delete(*keys)
    except Exception:
        pass


def flush_all():
    if not _r:
        return
    try:
        _r.flushdb()
    except Exception:
        pass
