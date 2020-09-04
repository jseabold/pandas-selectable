import pandas_select  # noqa


def test_accessor_registered(dta):
    assert hasattr(dta, 'select')
    assert hasattr(dta.select, 'A')
    assert hasattr(dta.select.B, 'dt')
    assert hasattr(dta.select.C, 'str')
    assert hasattr(dta.select, 'index')
    assert dir(dta.select) == ['A', 'B', 'C', 'D', 'index']


def test_select(dta):
    assert ((dta.select.A > 5).A > 5).all()
    assert ((dta.select.A >= 5).A >= 5).all()
    assert ((dta.select.A == 3).A == 3).any()
    assert ((dta.select.A < 3).A < 3).all()
    assert ((dta.select.A <= 3).A <= 3).all()
    assert ((dta.select.A != 3).A != 3).all()
    assert len(dta.select.A.isnull()) == 0
    assert len(dta.select.A.isna()) == 0
    assert len(dta.select.A.isin([5])) == 1


def test_str(dta):
    assert ((dta.select.C == 'A').C == 'A').all()
    assert ((dta.select.C < 'B').C == 'A').all()
    assert (dta.select.C <= 'B').C.isin(['A', 'B']).all()
    assert ((dta.select.C > 'B').C == 'C').all()
    assert (dta.select.C >= 'B').C.isin(['B', 'C']).all()
    assert (dta.select.C != 'B').C.isin(['A', 'C']).all()

    assert dta.select.C.str.contains('A').shape == (5, 4)
    assert (dta.select.C.str.contains('A').C == 'A').all()
    assert (dta.select.C.str.endswith('A').C == 'A').all()
    assert dta.select.C.str.isalnum().C.equals(dta.C)
    assert dta.select.C.str.isalpha().C.equals(dta.C)
    assert len(dta.select.C.str.isdecimal()) == 0
    assert len(dta.select.C.str.isdigit()) == 0
    assert len(dta.select.C.str.islower()) == 0
    assert len(dta.select.C.str.isnumeric()) == 0
    assert len(dta.select.C.str.isspace()) == 0
    assert dta.select.C.str.istitle().C.equals(dta.C)
    assert dta.select.C.str.isupper().C.equals(dta.C)
    assert (dta.select.C.str.match('A').C == 'A').all()
    assert (dta.select.C.str.startswith('A').C == 'A').all()


def test_dt(dta):
    assert dta.select.B.dt.is_leap_year.equals(dta)
    assert len(dta.select.B.dt.is_month_end) == 0
    assert dta.select.B.dt.is_month_start.equals(dta.loc[[0]])
    assert len(dta.select.B.dt.is_quarter_end) == 0
    assert dta.select.B.dt.is_quarter_start.equals(dta.loc[[0]])
    assert len(dta.select.B.dt.is_year_end) == 0
    assert dta.select.B.dt.is_year_start.equals(dta.loc[[0]])


def test_index(dta):
    assert (dta.select.index > 10).equals(dta.loc[dta.index > 10])
    assert (dta.select.index >= 10).equals(dta.loc[dta.index >= 10])
    assert (dta.select.index < 10).equals(dta.loc[dta.index < 10])
    assert (dta.select.index <= 10).equals(dta.loc[dta.index <= 10])
    assert (dta.select.index == 10).equals(dta.loc[dta.index == 10])
    assert (dta.select.index != 10).equals(dta.loc[dta.index != 10])

    assert len(dta.select.index.isna()) == 0
    assert len(dta.select.index.isnull()) == 0
    assert len(dta.select.index.isin([10, 11])) == 2


def test_series(dta):
    assert ((dta.A.select > 5) > 5).all()
    assert len(dta.B.select > '2020-01-02') == 13
    # the API here is slightly inconsistent
    assert dta.B.select.dt.is_leap_year.equals(dta.B)
    assert ((dta.C.select == 'A') == 'A').all()
    # the API here is slightly inconsistent
    assert (dta.C.select.str.contains('A') == 'A').all()
    assert ((dta.D.select == 'A') == 'A').all()
