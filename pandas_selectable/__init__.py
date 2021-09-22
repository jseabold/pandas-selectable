import inspect
import operator
from functools import wraps

import numpy as np
import pandas as pd
from pandas.core.accessor import CachedAccessor
from pandas.core.indexes.accessors import (
    CombinedDatetimelikeProperties,
    DatetimeProperties,
    PeriodProperties,
)
from pandas.core.strings import StringMethods
from pandas.util._decorators import doc

_str_boolean_methods = set(
    [
        'contains',
        'endswith',
        'isalnum',
        'isalpha',
        'isdecimal',
        'isdigit',
        'islower',
        'isnumeric',
        'isspace',
        'istitle',
        'isupper',
        'match',
        'startswith',
    ]
)

_date_boolean_methods = set(
    [
        'is_leap_year',
        'is_month_end',
        'is_month_start',
        'is_quarter_end',
        'is_quarter_start',
        'is_year_end',
        'is_year_start',
    ]
)


class StringSelectMethods(StringMethods):
    def __init__(self, *args, **kwargs):
        frame_or_series = args[0]

        # the superclass will override _parent, so we need to use _parent_frame
        self._parent_frame = frame_or_series._parent
        self._series = frame_or_series._series
        super().__init__(self._series, *args[1:], **kwargs)

    def __getattribute__(self, attr):
        if (
            not attr.startswith("_")
            and inspect.isroutine(getattr(StringMethods, attr, None))  # noqa
            and attr not in _str_boolean_methods
        ):  # noqa
            raise NotImplementedError(
                "Boolean selection with this method " "does not make sense."
            )
        else:
            return super().__getattribute__(attr)

    def _wrap_result(self, *args, **kwargs):
        # remove methods that don't return boolean index
        bool_idx = super()._wrap_result(*args, **kwargs)
        return self._parent_frame.loc[bool_idx]


class SelectPeriodProperties(PeriodProperties):
    def __init__(self, parent, *args, **kwargs):
        self._parent_frame = parent
        super().__init__(*args, **kwargs)

    @property
    def is_leap_year(self):
        return self._parent_frame.loc[super().is_leap_year]


class DateSelectMethods(CombinedDatetimelikeProperties):
    def __new__(cls, series):
        properties = super().__new__(cls, series._series)
        if isinstance(properties, DatetimeProperties):
            return SelectDatetimeProperties(
                series._parent, properties._parent, properties.orig
            )
        elif isinstance(properties, PeriodProperties):
            return SelectPeriodProperties(
                series._frame, properties._parent, properties.orig
            )
        raise AttributeError(
            "Can only use select.dt accessor on"
            "datetimelike and periodlike values."
        )


def selector_wrapper(klass, method_name):
    method = getattr(klass, method_name)

    @wraps(method)
    def selector(self, *args, **kwargs):
        # for a series accessor series and parent are the same thing
        # for a frame accessor we're indexing on the parent dataframe
        series = self._series
        idx = getattr(klass, method_name)(series, *args, **kwargs)
        return self._parent.loc[idx]

    return selector


class SelectableIndex:
    def __init__(self, parent):
        self._parent = parent
        self._index = parent.index

    def __getattr__(self, attr):
        return getattr(self._index, attr)

    def __repr__(self):
        return pd.Index.__repr__(self)

    def _compare(self, op, cmp):
        idx = op(self._parent.index, cmp)
        return self._parent.loc[idx]

    def __lt__(self, cmp):
        return self._compare(operator.lt, cmp)

    def __le__(self, cmp):
        return self._compare(operator.le, cmp)

    def __eq__(self, cmp):
        return self._compare(operator.eq, cmp)

    def __ne__(self, cmp):
        return self._compare(operator.ne, cmp)

    def __gt__(self, cmp):
        return self._compare(operator.gt, cmp)

    def __ge__(self, cmp):
        return self._compare(operator.ge, cmp)

    @doc(pd.Index.isna)
    def isna(self):
        return self._parent.loc[self._parent.index.isna()]

    @doc(pd.Index.isnull)
    def isnull(self):
        return self._parent.loc[self._parent.index.isnull()]

    @doc(pd.Index.notnull)
    def notnull(self):
        return self._parent.loc[self._parent.index.notnull()]

    @doc(pd.Index.notna)
    def notna(self):
        return self._parent.loc[self._parent.index.notna()]

    @doc(pd.Index.isin)
    def isin(self, values, levels=None):
        idx = self._parent.index.isin(values, levels)
        return self._parent.loc[idx]


@pd.api.extensions.register_series_accessor("select")
class SelectableColumn:
    str = CachedAccessor("str", StringSelectMethods)
    dt = CachedAccessor("dt", DateSelectMethods)

    __lt__ = selector_wrapper(pd.Series, "__lt__")
    __le__ = selector_wrapper(pd.Series, "__le__")
    __eq__ = selector_wrapper(pd.Series, "__eq__")
    __ne__ = selector_wrapper(pd.Series, "__ne__")
    __gt__ = selector_wrapper(pd.Series, "__gt__")
    __ge__ = selector_wrapper(pd.Series, "__ge__")
    isna = selector_wrapper(pd.Series, "isna")
    isnull = selector_wrapper(pd.Series, "isnull")
    notna = selector_wrapper(pd.Series, "notna")
    notnull = selector_wrapper(pd.Series, "notnull")
    isin = selector_wrapper(pd.Series, "isin")
    between = selector_wrapper(pd.Series, "between")

    def __init__(self, parent, series=None):
        # if accessed as the series accessor, parent is the series
        # if returned by a selectable dataframe, parent is the frame
        if series is None:
            series = parent
        self._parent = parent
        self._series = series

    def __getattr__(self, attr):
        return getattr(self._series, attr)

    def __repr__(self):
        return pd.Series.__repr__(self)

    @property
    def index(self):
        return SelectableIndex(self._parent)


@pd.api.extensions.register_dataframe_accessor('select')
class DataFrameSelectAccessor:
    def __init__(self, frame):
        self._frame = frame

    def __repr__(self):
        return pd.DataFrame.__repr__(self)

    def __dir__(self):
        return self._frame.columns.tolist() + ['index']

    def __getattr__(self, attr):
        if attr in self._frame.columns:
            return SelectableColumn(self._frame, self._frame[attr])
        return getattr(self._frame, attr)

    def __getitem__(self, key):
        try:
            getattr(self, key)
        except AttributeError:
            raise KeyError(f"{key}")

    @property
    def index(self):
        return SelectableIndex(self._frame)


class SelectDatetimeProperties(DatetimeProperties):
    def __init__(self, parent, *args, **kwargs):
        # datetime properties holds an attribute _parent
        # we need to add the parent_frame (or series) to the subclass instances
        self._parent_frame = parent
        super().__init__(*args, **kwargs)

    def __getattribute__(self, attr):
        if (
            not attr.startswith("_")
            and inspect.isroutine(  # noqa
                getattr(DatetimeProperties, attr, None)
            )
            and attr not in _date_boolean_methods
        ):  # noqa
            raise NotImplementedError(
                "Boolean selection with this method " "does not make sense."
            )
        elif attr in _date_boolean_methods:
            idx = super().__getattribute__(attr)
            return self._parent_frame.loc[idx]
        else:
            got_attr = super().__getattribute__(attr)
            # this allows things like dt.day, dt.month to be selectable
            # for the parent frame. assumes they're all properties.
            if (
                isinstance(got_attr, pd.Series)
                and not attr.startswith('_')
                and isinstance(getattr(self.__class__, attr), property)
            ):
                return SelectableColumn(self._parent_frame, got_attr)
            return got_attr
