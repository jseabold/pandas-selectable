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
   ...:     'A': ['A', 'B', 'C'] * 5,
   ...:     'B': np.arange(1, 16),
   ...:     'C': pd.date_range('2020-01-01', periods=15)
   ...: })

In [5]: dta.head()
Out[5]:
   A  B          C
0  A  1 2020-01-01
1  B  2 2020-01-02
2  C  3 2020-01-03
3  A  4 2020-01-04
4  B  5 2020-01-05

In [6]: dta.select.A == 'B'
Out[6]:
    A   B          C
1   B   2 2020-01-02
4   B   5 2020-01-05
7   B   8 2020-01-08
10  B  11 2020-01-11
13  B  14 2020-01-14

In [7]: dta.select.C >= '2020-01-03'
Out[7]:
    A   B          C
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

In [8]: dta.select.A.str.contains('A')
Out[8]:
    A   B          C
0   A   1 2020-01-01
3   A   4 2020-01-04
6   A   7 2020-01-07
9   A  10 2020-01-10
12  A  13 2020-01-13

In [9]: dta.select.C.dt.is_month_start
Out[9]:
   A  B          C
0  A  1 2020-01-01
```

It also works for Series.

```python
In [10]: dta.A.select == 'A'
Out[10]:
0     A
3     A
6     A
9     A
12    A
Name: A, dtype: object
```

Though the string and datetime accessor APIs are slightly inconsistent. They're available via the select accessor now.

```python
In [11]: dta.A.select.str.contains('B')
Out[11]:
1     B
4     B
7     B
10    B
13    B
Name: A, dtype: object
```

## Requirements

[pandas](https://pandas.pydata.org/) >= 1.1

## Installation

```bash
pip install pandas-selectable
```
