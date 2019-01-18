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
                               details=None,
                               transform=None):

    _MSG_KEYS = {'old_param': old_param,
                 'new_param': new_param,
                 'deprecated_in': deprecated_in,
                 'removed_in': removed_in,
                 'old_param': old_param,
                 'new_param': new_param,
                 'details': details}
    _MSG = ('`{old_param}` is deprecated and will be replaced by `{new_param}`'
            ' in {deprecated_in}. `{old_param}` will be no longer present'
            ' starting in {removed_in}. {details}').format(**_MSG_KEYS)

    def true_decorator(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            warn(_MSG, DeprecationWarning)
            if transform is None:
                kwargs[new_param] = kwargs.pop(old_param)
            else:
                kwargs[new_param] = transform(kwargs.pop(old_param))

            r = f(*args, **kwargs)
            return r
        return wrapped
    return true_decorator


@deprecate_parameter_rename(deprecated_in="1.0", removed_in="2.0",
                            current_version=__version__,
                            old_param='foo', new_param='bar',
                            transform=None,
                            details="some extra details")
def my_function_C(bar=None):
    return bar


def test_my_function_A_depracation():
    with pytest.deprecated_call(match="my_new_function"):
        my_function_A()


def test_old_param_in_my_function_B_deprecation():
    with pytest.deprecated_call(match="old_param .* new_param"):
        my_function_B(old_param='bar')


def test_foo():
    with pytest.deprecated_call() as record:
        xx = my_function_C(foo='ups')  # call with old parameter
    assert xx == 'ups'
    print(record.list[0].message)
