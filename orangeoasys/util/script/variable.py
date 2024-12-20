from math import isnan, floor
from numbers import Real

from orangeoasys.util.script.value import Value, Unknown
import collections


ValueUnknown = Unknown  # Shadowing within classes


class Variable:
    """
    The base class for variable descriptors contains the variable's
    name and some basic properties.

    .. attribute:: name

        The name of the variable.

    .. attribute:: unknown_str

        A set of values that represent unknowns in conversion from textual
        formats. Default is `{"?", ".", "", "NA", "~", None}`.

    .. attribute:: compute_value

        A function for computing the variable's value when converting from
        another domain which does not contain this variable. The base class
        defines a static method `compute_value`, which returns `Unknown`.
        Non-primitive variables must redefine it to return `None`.

    .. attribute:: source_variable

        An optional descriptor of the source variable - if any - from which
        this variable is derived and computed via :obj:`compute_value`.

    .. attribute:: attributes

        A dictionary with user-defined attributes of the variable
    """

    _DefaultUnknownStr = {"?", ".", "", "NA", "~", None}

    _variable_types = []
    Unknown = ValueUnknown


    def __init__(self, name="", compute_value=None):
        """
        Construct a variable descriptor.
        """
        self.name = name
        if compute_value is not None:
            self.compute_value = compute_value
        self.unknown_str = set(Variable._DefaultUnknownStr)
        self.source_variable = None
        self.attributes = {}

    @staticmethod
    def is_primitive():
        """
        `True` if the variable's values are stored as floats.
        Primitive variables are :obj:`~data.DiscreteVariable` and
        :obj:`~data.ContinuousVariable`. Non-primitive variables can appear
        in the data only as meta attributes.

        Derived classes must overload the function.
        """
        raise RuntimeError("variable descriptors must overload is_primitive()")

    def repr_val(self, val):
        """
        Return a textual representation of variable's value `val`. Argument
        `val` must be a float (for primitive variables) or an arbitrary
        Python object (for non-primitives).

        Derived classes must overload the function.
        """
        raise RuntimeError("variable descriptors must overload repr_val()")

    str_val = repr_val

    def to_val(self, s):
        """
        Convert the given argument to a value of the variable. The
        argument can be a string, a number or `None`. For primitive variables,
        the base class provides a method that returns
        :obj:`~Orange.data.value.Unknown` if `s` is found in
        :obj:`~Orange.data.Variable.unknown_str`, and raises an exception
        otherwise. For non-primitive variables it returns the argument itself.

        Derived classes of primitive variables must overload the function.

        :param s: value, represented as a number, string or `None`
        :type s: str, float or None
        :rtype: float or object
        """
        if not self.is_primitive():
            return s
        if s in self.unknown_str:
            return Unknown
        raise RuntimeError(
            "primitive variable descriptors must overload to_val()")

    def val_from_str_add(self, s):
        """
        Convert the given string to a value of the variable. The method
        is similar to :obj:`to_val` except that it only accepts strings and
        that it adds new values to the variable's domain where applicable.

        The base class method calls `to_val`.

        :param s: symbolic representation of the value
        :type s: str
        :rtype: float or object
        """
        return self.to_val(s)

    def __str__(self):
        """
        Return a representation of the variable, like,
        `'DiscreteVariable("gender")'`. Derived classes may overload this
        method to provide a more informative representation.
        """
        return "{}('{}')".format(self.__class__.__name__, self.name)

    __repr__ = __str__

    @staticmethod
    def compute_value(_):
        return Unknown

    @classmethod
    def _clear_cache(cls):
        for tpe in cls._variable_types:
            tpe._clear_cache()


class ContinuousVariable(Variable):
    """
    Descriptor for continuous variables.

    .. attribute:: number_of_decimals

        The number of decimals when the value is printed out (default: 3).

    .. attribute:: adjust_decimals

        A flag regulating whether the `number_of_decimals` is being adjusted
        by :obj:`to_val`.

    The value of `number_of_decimals` is set to 3 and `adjust_decimals`
    is set to 2. When :obj:`val_from_str_add` is called for the first
    time with a string as an argument, `number_of_decimals` is set to the
    number of decimals in the string and `adjust_decimals` is set to 1.
    In the subsequent calls of `to_val`, the nubmer of decimals is
    increased if the string argument has a larger number of decimals.

    If the `number_of_decimals` is set manually, `adjust_decimals` is
    set to 0 to prevent changes by `to_val`.
    """
    all_continuous_vars = {}

    def __init__(self, name="", number_of_decimals=None):
        """
        Construct a new continuous variable. The number of decimals is set to
        three, but adjusted at the first call of :obj:`to_val`.
        """
        super().__init__(name)
        if number_of_decimals is None:
            self.number_of_decimals = 3
            self.adjust_decimals = 2
        else:
            self.number_of_decimals = number_of_decimals
        ContinuousVariable.all_continuous_vars[name] = self

    @property
    def number_of_decimals(self):
        return self._number_of_decimals

    # noinspection PyAttributeOutsideInit
    @number_of_decimals.setter
    def number_of_decimals(self, x):
        self._number_of_decimals = x
        self.adjust_decimals = 0
        self._out_format = "%.{}f".format(self.number_of_decimals)

    @staticmethod
    def make(name):
        """
        Return an existing continuous variable with the given name, or
        construct and return a new one.
        """
        existing_var = ContinuousVariable.all_continuous_vars.get(name)
        return existing_var or ContinuousVariable(name)

    @classmethod
    def _clear_cache(cls):
        """
        Clears the list of variables for reuse by :obj:`make`.
        """
        cls.all_continuous_vars.clear()

    @staticmethod
    def is_primitive():
        """ Return `True`: continuous variables are stored as floats."""
        return True

    def to_val(self, s):
        """
        Convert a value, given as an instance of an arbitrary type, to a float.
        """
        if s in self.unknown_str:
            return Unknown
        return float(s)

    def val_from_str_add(self, s):
        """
        Convert a value from a string and adjust the number of decimals if
        `adjust_decimals` is non-zero.
        """
        if s in self.unknown_str:
            return Unknown
        val = float(s)  # raise exception before setting the number of decimals
        if self.adjust_decimals and isinstance(s, str):
            #TODO: This may significantly slow down file reading.
            #      Is there something we can do about it?
            s = s.strip()
            i = s.find(".")
            ndec = len(s) - i - 1 if i > 0 else 0
            if self.adjust_decimals == 2:
                self.number_of_decimals = ndec
            elif ndec > self.number_of_decimals:
                self.number_of_decimals = ndec
            self.adjust_decimals = 1
        return val

    def repr_val(self, val):
        """
        Return the value as a string with the prescribed number of decimals.
        """
        if isnan(val):
            return "?"
        return self._out_format % val

    str_val = repr_val


class DiscreteVariable(Variable):
    """
    Descriptor for symbolic, discrete variables. Values of discrete variables
    are stored as floats; the numbers corresponds to indices in the list of
    values.

    .. attribute:: values

        A list of variable's values.

    .. attribute:: ordered

        Some algorithms (and, in particular, visualizations) may
        sometime reorder the values of the variable, e.g. alphabetically.
        This flag hints that the given order of values is "natural"
        (e.g. "small", "middle", "large") and should not be changed.

    .. attribute:: base_value

        The index of the base value, or -1 if there is none. The base value is
        used in some methods like, for instance, when creating dummy variables
        for regression.
    """
    all_discrete_vars = collections.defaultdict(set)
    presorted_values = []

    def __init__(self, name="", values=(), ordered=False, base_value=-1):
        """ Construct a discrete variable descriptor with the given values. """
        super().__init__(name)
        self.ordered = ordered
        self.values = list(values)
        self.base_value = base_value
        DiscreteVariable.all_discrete_vars[name].add(self)

    def __str__(self):
        """
        Give a string representation of the variable, for instance,
        `"DiscreteVariable('Gender', values=['male', 'female'])"`.
        """
        args = "values=[" + ", ".join(self.values[:5]) +\
               "..." * (len(self.values) > 5) + "]"
        if self.ordered:
            args += ", ordered=True"
        if self.base_value >= 0:
            args += ", base_value={}".format(self.base_value)
        return "{}('{}', {})".format(self.__class__.__name__, self.name, args)

    @staticmethod
    def is_primitive():
        """ Return `True`: discrete variables are stored as floats. """
        return True

    def to_val(self, s):
        """
        Convert the given argument to a value of the variable (`float`).
        If the argument is numeric, its value is returned without checking
        whether it is integer and within bounds. `Unknown` is returned if the
        argument is one of the representations for unknown values. Otherwise,
        the argument must be a string and the method returns its index in
        :obj:`values`.

        :param s: values, represented as a number, string or `None`
        :rtype: float
        """
        if s is None:
            return ValueUnknown

        if isinstance(s, int):
            return s
        if isinstance(s, Real):
            return s if isnan(s) else floor(s + 0.25)
        if s in self.unknown_str:
            return ValueUnknown
        if not isinstance(s, str):
            raise TypeError('Cannot convert {} to value of "{}"'.format(
                type(s).__name__, self.name))
        return self.values.index(s)

    def add_value(self, s):
        """ Add a value `s` to the list of values.
        """
        self.values.append(s)

    def val_from_str_add(self, s):
        """
        Similar to :obj:`to_val`, except that it accepts only strings and that
        it adds the value to the list if it does not exist yet.

        :param s: symbolic representation of the value
        :type s: str
        :rtype: float
        """
        try:
            return ValueUnknown if s in self.unknown_str \
                else self.values.index(s)
        except ValueError:
            self.add_value(s)
            return len(self.values) - 1

    def repr_val(self, val):
        """
        Return a textual representation of the value (`self.values[int(val)]`)
        or "?" if the value is unknown.

        :param val: value
        :type val: float (should be whole number)
        :rtype: str
        """
        if isnan(val):
            return "?"
        return '{}'.format(self.values[int(val)])

    str_val = repr_val

    @staticmethod
    def make(name, values=(), ordered=False, base_value=-1):
        """
        Return a variable with the given name and other properties. The method
        first looks for a compatible existing variable: the existing
        variable must have the same name and both variables must have either
        ordered or unordered values. If values are ordered, the order must be
        compatible: all common values must have the same order. If values are
        unordered, the existing variable must have at least one common value
        with the new one, except when any of the two lists of values is empty.

        If a compatible variable is find, it is returned, with missing values
        appended to the end of the list. If there is no explicit order, the
        values are ordered using :obj:`ordered_values`. Otherwise, it
        constructs and returns a new variable descriptor.

        :param name: the name of the variable
        :type name: str
        :param values: symbolic values for the variable
        :type values: list
        :param ordered: tells whether the order of values is fixed
        :type ordered: bool
        :param base_value: the index of the base value, or -1 if there is none
        :type base_value: int
        :returns: an existing compatible variable or `None`
        """
        var = DiscreteVariable._find_compatible(
            name, values, ordered, base_value)
        if var:
            return var
        if not ordered:
            base_value_rep = base_value != -1 and values[base_value]
            values = DiscreteVariable.ordered_values(values)
            if base_value != -1:
                base_value = values.index(base_value_rep)
        return DiscreteVariable(name, values, ordered, base_value)

    @staticmethod
    def _find_compatible(name, values=(), ordered=False, base_value=-1):
        """
        Return a compatible existing value, or `None` if there is None.
        See :obj:`make` for details; this function differs by returning `None`
        instead of constructing a new descriptor. (Method :obj:`make` calls
        this function.)

        :param name: the name of the variable
        :type name: str
        :param values: symbolic values for the variable
        :type values: list
        :param ordered: tells whether the order of values is fixed
        :type ordered: bool
        :param base_value: the index of the base value, or -1 if there is none
        :type base_value: int
        :returns: an existing compatible variable or `None`
        """
        base_rep = base_value != -1 and values[base_value]
        existing = DiscreteVariable.all_discrete_vars.get(name)
        if existing is None:
            return None
        if not ordered:
            values = DiscreteVariable.ordered_values(values)
        for var in existing:
            if (var.ordered != ordered or
                    var.base_value != -1
                    and var.values[var.base_value] != base_rep):
                continue
            if not values:
                break  # we have the variable - any existing values are OK
            if ordered:
                i = 0
                for val in var.values:
                    if values[i] == val:
                        i += 1
                        if i == len(values):
                            break  # we have all the values
                else:  # we have some remaining values: check them, add them
                    if set(values[i:]) & set(var.values):
                        continue  # next var in existing
                    for val in values[i:]:
                        var.add_value(val)
                break  # we have the variable
            else:  # not ordered
                if var.values and not set(var.values) & set(values):
                    continue  # empty intersection of values; not compatible
                vv = set(var.values)
                for val in values:
                    if val not in vv:
                        var.add_value(val)
                break  # we have the variable
        else:
            return None
        if base_value != -1 and var.base_value == -1:
            var.base_value = var.values.index(base_rep)
        return var

    @classmethod
    def _clear_cache(cls):
        """
        Clears the list of variables for reuse by :obj:`make`.
        """
        cls.all_discrete_vars.clear()

    @staticmethod
    def ordered_values(values):
        """
        Return a sorted list of values. If there exists a prescribed order for
        such set of values, it is returned. Otherwise, values are sorted
        alphabetically.
        """
        for presorted in DiscreteVariable.presorted_values:
            if values == set(presorted):
                return presorted
        return sorted(values)


class StringVariable(Variable):
    """
    Descriptor for string variables. String variables can only appear as
    meta attributes.
    """
    all_string_vars = {}
    Unknown = None

    def __init__(self, name="", default_col=-1):
        """Construct a new descriptor."""
        super().__init__(name)
        StringVariable.all_string_vars[name] = self

    @staticmethod
    def is_primitive():
        """Return `False`: string variables are not stored as floats."""
        return False

    @staticmethod
    def compute_value(_):
        return None

    def to_val(self, s):
        """
        Return the value as a string. If it is already a string, the same
        object is returned.
        """
        if s is None:
            return ""
        if isinstance(s, str):
            return s
        return str(s)

    val_from_str_add = to_val

    def str_val(self, val):
        """Return a string representation of the value."""
        if isinstance(val, Value):
            if val.value is None:
                return "None"
            val = val.value
        return str(val)

    def repr_val(self, val):
        """Return a string representation of the value."""
        return '"{}"'.format(self.str_val(val))

    @staticmethod
    def make(name):
        """
        Return an existing string variable with the given name, or construct
        and return a new one.
        """
        existing_var = StringVariable.all_string_vars.get(name)
        return existing_var or StringVariable(name)

    @classmethod
    def _clear_cache(cls):
        """
        Clears the list of variables for reuse by :obj:`make`.
        """
        cls.all_string_vars.clear()

Variable._variable_types += [DiscreteVariable, ContinuousVariable, StringVariable
    ]
