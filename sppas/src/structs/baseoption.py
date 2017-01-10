# -*- coding: UTF-8 -*-
# ---------------------------------------------------------------------------
#            ___   __    __    __    ___
#           /     |  \  |  \  |  \  /              the automatic
#           \__   |__/  |__/  |___| \__             annotation and
#              \  |     |     |   |    \             analysis
#           ___/  |     |     |   | ___/              of speech
#
#
#                           http://www.sppas.org/
#
# ---------------------------------------------------------------------------
#            Laboratoire Parole et Langage, Aix-en-Provence, France
#                   Copyright (C) 2011-2017  Brigitte Bigi
#
#                   This banner notice must not be removed
# ---------------------------------------------------------------------------
# Use of this software is governed by the GNU Public License, version 3.
#
# SPPAS is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SPPAS is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with SPPAS. If not, see <http://www.gnu.org/licenses/>.
#
# ---------------------------------------------------------------------------
# File: src.structs.baseoption.py
# ----------------------------------------------------------------------------

from sp_glob import encoding

# ----------------------------------------------------------------------------


class sppasBaseOption(object):
    """
    @author:       Brigitte Bigi
    @organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    @contact:      brigitte.bigi@gmail.com
    @license:      GPL, v3
    @copyright:    Copyright (C) 2011-2017  Brigitte Bigi
    @summary:      Class to deal with one option.

    An option is a set of data with a main value and its type, then 3 other
    variables to store any kind of information. By default, the type of an
    option is "str", the value is an empty string and the name, text and
    description are all empty strings.

    >>> o = sppasBaseOption("integer", "3")
    >>> v = o.get_value()
    >>> type(v)
    >>> <type 'int'>
    >>> v = o.get_untypedvalue()
    >>> type(v)
    >>> <type 'str'>

    """
    def __init__(self, option_type, option_value=""):
        """
        Creates a new option instance.

        :param option_type: (str) Type of the option (i.e. 'int', 'bool', 'float', ...).
        Notice that the type will be normalized. For example, 'int, 'integer', 'long or
        'short' will be all stored into 'int' type.
        :param option_value (str) The value of the option.

        """
        self._type = ""
        self.set_type(option_type)
        self._value = option_value
        self._text = ""
        self._name = ""
        self._description = ""

    # ------------------------------------------------------------------------
    # Getters
    # ------------------------------------------------------------------------

    def get_type(self):
        """
        Return the type of the option.

        :returns: normalized value of the type

        """
        return self._type

    # ------------------------------------------------------------------------

    def get_untypedvalue(self):
        """
        Return the value as it was given,
        i.e. without taking the given type into account.

        """
        return self._value

    # ------------------------------------------------------------------------

    def get_value(self):
        """ Return the typed-value or None if the type is unknown. """

        if self._type == "bool":
            if isinstance(self._value, bool):
                return self._value
            if self._value.lower() == "true":
                return True
            return False

        elif self._type == 'int':
            return int(self._value)

        elif self._type == 'float':
            return float(self._value)

        elif self._type == 'str' or self._type.startswith("file"):
            return self._value.decode(encoding)

        return None

    # ------------------------------------------------------------------------

    def get_name(self):
        """ Return the name of to this option. """

        return self._name

    # ------------------------------------------------------------------------

    def get_text(self):
        """ Return the brief text which describes the option. """

        return self._text

    # ------------------------------------------------------------------------

    def get_description(self):
        """ Return the long text which describes the option. """

        return self._description

    # ------------------------------------------------------------------------
    # Setters
    # ------------------------------------------------------------------------

    def set(self, other):
        """
        Set self from another instance.

        :param other: (baseoption) The option from which to get information.

        """
        self._type = other.get_type()
        self._value = other.get_untypedvalue()
        self._text = other.get_text()
        self._name = other.get_name()
        self._description = other.get_description()

    # ------------------------------------------------------------------------

    def set_type(self, option_type):
        """
        Set a new type.

        :param option_type: (str) Type of the option (i.e. 'int', 'bool', 'float', ...).
        If the option_type is not valid, type will be set to 'str'.
        :returns: True if option_type is valid and set.

        """

        option_type = option_type.lower()

        if option_type.startswith('bool'):
            self._type = "bool"
            return True

        elif option_type.startswith('int') or option_type == 'long' or option_type == 'short':
            self._type = "int"
            return True

        elif option_type == 'float' or option_type == 'double':
            self._type = "float"
            return True

        elif "file" in option_type:
            if "name" in option_type:
                self._type = "filename"
                return True

            elif "path" in option_type:
                self._type = "filepath"
                return True

        self._type = "str"
        return False

    # ------------------------------------------------------------------------

    def set_value(self, value):
        """
        Set a new value.

        :param value: (any type) Un-typed value of the option.

        """
        self._value = value

    # ------------------------------------------------------------------------

    def set_name(self, name):
        """
        Set a name text which describes the option.

        :param name: (str) Option description.

        """
        self._name = name

    # ------------------------------------------------------------------------

    def set_text(self, text):
        """
        Set a brief text which describes the option.

        :param text: (str) Option description.

        """
        self._text = text

    # ------------------------------------------------------------------------

    def set_description(self, description):
        """
        Set a long text which describes the option.

        :param description: (str) Option description.

        """
        self._description = description

# ----------------------------------------------------------------------------


class Option(sppasBaseOption):
    """
    @author:       Brigitte Bigi
    @organization: Laboratoire Parole et Langage, Aix-en-Provence, France
    @contact:      brigitte.bigi@gmail.com
    @license:      GPL, v3
    @copyright:    Copyright (C) 2011-2017  Brigitte Bigi
    @summary:      Class that adds a key as identifier to a sppasBaseOption.

    """
    def __init__(self, option_key, option_type="str", option_value=""):
        """
        Instantiate an Option.

        :param option_key: (any type) An identifier for that option.

        """
        sppasBaseOption.__init__(self, option_type, option_value)
        self._key = option_key

    # ----------------------------------------------------------------------------

    def get_key(self):
        """ Return the key of that option. """

        return self._key

# ----------------------------------------------------------------------------
