cdef extern from 'Python.h':
    cdef int PyTuple_SET_ITEM(tuple, int, object)
    cdef tuple PyTuple_New(int)
    cdef void Py_INCREF(object)
    cdef void Py_DECREF(object)

cdef class MultiFunctionBase(object):

    '''Implements a multi argument dispatch function.'''

    cdef dict _c_cache

    def __init__(MultiFunctionBase self, name='', doc=None):
        self._init(name, doc)

    def _init(MultiFunctionBase self, name, doc):
        self._data = {}
        self._c_cache = {}
        self._name = name
        self._doc = doc

    def __call__(MultiFunctionBase self, *args, **kwargs):
        "Resolve and dispatch to best method."

        cdef int N = len(args), M = len(kwargs)
        cdef tuple types = PyTuple_New(N)
        for i in range(N):
            PyTuple_SET_ITEM(types, i, type(args[i]))
        Py_INCREF(types)

        try:
            func = self._c_cache[types]
        except KeyError:
            func = self.get_function(*types)

        if M == 0:
            return func(*args)
        else:
            return func(*args, **kwargs)

    property _cache:
        def __get__(MultiFunctionBase self):
            return self._c_cache