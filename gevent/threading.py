__implements__ = ['local',
                  '_start_new_thread',
                  '_allocate_lock',
                  'Lock',
                  '_sleep',
                  '_DummyThread']


import threading as __threading__
_DummyThread_ = __threading__._DummyThread
from gevent.local import local
from gevent.thread import start_new_thread as _start_new_thread, allocate_lock as _allocate_lock
from gevent.hub import sleep as _sleep, getcurrent, PY3
if PY3:
    from gevent.thread import get_ident
    __implements__.append('get_ident')
else:
    from gevent.thread import get_ident as _get_ident
    __implements__.append('_get_ident')
Lock = _allocate_lock


def _cleanup(g):
    __threading__._active.pop(id(g))


class _DummyThread(_DummyThread_):
    # instances of this will cleanup its own entry
    # in ``threading._active``

    def __init__(self):
        _DummyThread_.__init__(self)
        g = getcurrent()
        rawlink = getattr(g, 'rawlink', None)
        if rawlink is not None:
            rawlink(_cleanup)
