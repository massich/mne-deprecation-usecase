from mne.utils import deprecated
from mne.utils import warn
from functools import wraps

import pytest

__version__ = 1.5


@deprecated('my_function will be deprecated in 0.XX,'
            ' please use my_new_function instead.')
def my_function_A():
    return 'foo'


def my_function_B(new_param=None, old_param='not_used'):
    if old_param != 'not_used':
        warn(('old_param is deprecated and will be replaced'
              ' by new_param in 0.XX.'), DeprecationWarning)
    new_param = old_param  # noqa
    # Do what you have to do with new_param
    return 'foo'


def deprecate_parameter_rename(deprecated_in, removed_in,
                               current_version,
                               old_param, new_param,
                               details,
                               transform=None):
    def true_decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # import pdb; pdb.set_trace()
            _MSG = 'something based ont he dec params'
            warn(_MSG, DeprecationWarning)
            kwargs['bar'] = kwargs.pop('foo')
            r = f(*args, **kwargs)
            return r
        return wrapped
    return true_decorator


@deprecate_parameter_rename(deprecated_in="1.0", removed_in="2.0",
                            current_version=__version__,
                            old_param='foo', new_param='bar',
                            transform=None,
                            details="Use the bar function instead")
def my_function_C(bar=None):
    return bar


def test_my_function_A_depracation():
    with pytest.deprecated_call(match="my_new_function"):
        my_function_A()


def test_old_param_in_my_function_B_deprecation():
    with pytest.deprecated_call(match="old_param .* new_param"):
        my_function_B(old_param='bar')


def test_foo():
    with pytest.deprecated_call():
        xx = my_function_C(foo='ups')  # call with old parameter
    assert xx == 'ups'
