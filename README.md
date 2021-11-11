# pandas-selectable

![test status](https://github.com/jseabold/pandas-selectable/workflows/tests/badge.svg)

## What Is It?

`pandas-selectable` adds a `select` accessor to pandas DataFrames and Series. It's like `query` but with the niceties of tab-completion.

## Quickstart

```python
In [1]: import numpy as np

In [2]: import pandas as pd

In [3]: import pandas_selectable  # magic

In [4]: dta = pd.DataFrame.from_dict({
   ...:     'X': ['A', 'B', 'C'] * 5,
   ...:     'Y': np.arange(1, 16),
   ...:     'Z': pd.date_range('2020-01-01', periods=15)
   ...: })

In [5]: dta.head()
Out[5]:
   X  Y          Z
0  A  1 2020-01-01
1  B  2 2020-01-02
2  C  3 2020-01-03
3  A  4 2020-01-04
4  B  5 2020-01-05

In [6]: dta.select.X == 'B'
Out[6]:
    X   Y          Z
1   B   2 2020-01-02
4   B   5 2020-01-05
7   B   8 2020-01-08
10  B  11 2020-01-11
13  B  14 2020-01-14

In [7]: dta.select.Z >= '2020-01-03'
Out[7]:
    X   Y          Z
2   C   3 2020-01-03
3   A   4 2020-01-04
4   B   5 2020-01-05
5   C   6 2020-01-06
6   A   7 2020-01-07
7   B   8 2020-01-08
8   C   9 2020-01-09
9   A  10 2020-01-10
10  B  11 2020-01-11
11  C  12 2020-01-12
12  A  13 2020-01-13
13  B  14 2020-01-14
14  C  15 2020-01-15

In [8]: dta.select.X.str.contains('A')
Out[8]:
    X   Y          Z
0   A   1 2020-01-01
3   A   4 2020-01-04
6   A   7 2020-01-07
9   A  10 2020-01-10
12  A  13 2020-01-13

In [9]: dta.select.Z.dt.is_month_start
Out[9]:
   X  Y          Z
0  A  1 2020-01-01
```

It also works for Series.

```python
In [10]: dta.X.select == 'A'
Out[10]:
0     A
3     A
6     A
9     A
12    A
Name: X, dtype: object
```

Though the string and datetime accessor APIs are slightly inconsistent. They're available via the select accessor now.

```python
In [11]: dta.X.select.str.contains('B')
Out[11]:
1     B
4     B
7     B
10    B
13    B
Name: X, dtype: object
```

## Requirements

[pandas](https://pandas.pydata.org/) >= 1.1

## Installation

```bash
pip install pandas-selectable
```
