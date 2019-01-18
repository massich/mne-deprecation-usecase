from mne.utils import deprecated
from mne.utils import warn

import pytest


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


def test_my_function_A_depracation():
    with pytest.deprecated_call(match="my_new_function"):
        my_function_A()


def test_old_param_in_my_function_B_deprecation():
    with pytest.deprecated_call(match="old_param .* new_param"):
        my_function_B(old_param='bar')
