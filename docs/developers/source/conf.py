# -*- coding: utf-8 -*-
#pylint: disable=C0103
#pylint: disable=W0622
#pylint: disable=W0212
#pylint: disable=W0613
  
import sys, os

on_rtd = os.environ.get('READTHEDOCS', None) == 'True'

sys.path.append('../../../')

from docs.shared.conf import *


# Add any paths that contain templates here, relative to this directory.
templates_path.append('source/_templates')


# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path.append('source/_static')


# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#sys.path.insert(0, os.path.abspath('../../..'))
root = os.path.abspath('../../..')

sys.path.append(root)
sys.path.append(os.path.join(root, "common/djangoapps"))
sys.path.append(os.path.join(root, "common/lib"))
sys.path.append(os.path.join(root, "common/lib/sandbox-packages"))
sys.path.append(os.path.join(root, "lms/djangoapps"))
sys.path.append(os.path.join(root, "lms/lib"))
sys.path.append(os.path.join(root, "cms/djangoapps"))
sys.path.append(os.path.join(root, "cms/lib"))
sys.path.insert(0, os.path.abspath(os.path.normpath(os.path.dirname(__file__)
    + '/../../')))
sys.path.append('.')

#  django configuration  - careful here
if on_rtd:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'lms'
else:
    os.environ['DJANGO_SETTINGS_MODULE'] = 'lms.envs.test'


# -- General configuration -----------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be extensions
# coming with Sphinx (named 'sphinx.ext.*') or your custom ones.
extensions = [
    'sphinx.ext.autodoc', 'sphinx.ext.doctest', 'sphinx.ext.intersphinx', 'sphinx.ext.todo', 'sphinx.ext.coverage',
    'sphinx.ext.pngmath', 'sphinx.ext.mathjax', 'sphinx.ext.viewcode']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['build']


# Output file base name for HTML help builder.
htmlhelp_basename = 'edXDocs'


# from http://djangosnippets.org/snippets/2533/
# autogenerate models definitions

import inspect
import types
from HTMLParser import HTMLParser


def force_unicode(s, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Similar to smart_unicode, except that lazy instances are resolved to
    strings, rather than kept as lazy objects.

    If strings_only is True, don't convert (some) non-string-like objects.
    """
    if strings_only and isinstance(s, (types.NoneType, int)):
        return s
    if not isinstance(s, basestring,):
        if hasattr(s, '__unicode__'):
            s = unicode(s)
        else:
            s = unicode(str(s), encoding, errors)
    elif not isinstance(s, unicode):
        s = unicode(s, encoding, errors)
    return s


class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()

class Mock(object):
    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        return Mock()

    @classmethod
    def __getattr__(cls, name):
        if name in ('__file__', '__path__'):
            return '/dev/null'
        elif name[0] == name[0].upper():
            mockType = type(name, (), {})
            mockType.__module__ = __name__
            return mockType
        else:
            return Mock()

MOCK_MODULES = ['scipy', 'numpy']
for mod_name in MOCK_MODULES:
    sys.modules[mod_name] = Mock()

def process_docstring(app, what, name, obj, options, lines):
    """Autodoc django models"""

    # This causes import errors if left outside the function
    from django.db import models

    # If you want extract docs from django forms:
    # from django import forms
    # from django.forms.models import BaseInlineFormSet

    # Only look at objects that inherit from Django's base MODEL class
    if inspect.isclass(obj) and issubclass(obj, models.Model):
        # Grab the field list from the meta class
        fields = obj._meta._fields()

        for field in fields:
            # Decode and strip any html out of the field's help text
            help_text = strip_tags(force_unicode(field.help_text))

            # Decode and capitalize the verbose name, for use if there isn't
            # any help text
            verbose_name = force_unicode(field.verbose_name).capitalize()

            if help_text:
                # Add the model field to the end of the docstring as a param
                # using the help text as the description
                lines.append(u':param %s: %s' % (field.attname, help_text))
            else:
                # Add the model field to the end of the docstring as a param
                # using the verbose name as the description
                lines.append(u':param %s: %s' % (field.attname, verbose_name))

            # Add the field's type to the docstring
            lines.append(u':type %s: %s' % (field.attname, type(field).__name__))
        # Only look at objects that inherit from Django's base FORM class
    # elif (inspect.isclass(obj) and issubclass(obj, forms.ModelForm) or issubclass(obj, forms.ModelForm) or issubclass(obj, BaseInlineFormSet)):
    #     pass
        # # Grab the field list from the meta class
        # import ipdb; ipdb.set_trace()
        # fields = obj._meta._fields()
        # import ipdb; ipdb.set_trace()
        # for field in fields:
        #     import ipdb; ipdb.set_trace()
        #     # Decode and strip any html out of the field's help text
        #     help_text = strip_tags(force_unicode(field.help_text))

        #     # Decode and capitalize the verbose name, for use if there isn't
        #     # any help text
        #     verbose_name = force_unicode(field.verbose_name).capitalize()

        #     if help_text:
        #         # Add the model field to the end of the docstring as a param
        #         # using the help text as the description
        #         lines.append(u':param %s: %s' % (field.attname, help_text))
        #     else:
        #         # Add the model field to the end of the docstring as a param
        #         # using the verbose name as the description
        #         lines.append(u':param %s: %s' % (field.attname, verbose_name))

        #     # Add the field's type to the docstring
        #     lines.append(u':type %s: %s' % (field.attname, type(field).__name__))
    # Return the extended docstring
    return lines


def setup(app):
    """Setup docsting processors"""
    #Register the docstring processor with sphinx
    app.connect('autodoc-process-docstring', process_docstring)
