import numpy as np
import pandas as pd
import pytest


@pytest.fixture
def dta():
    return pd.DataFrame.from_dict({
        'A': np.arange(1, 16),
        'B': pd.date_range('2020-01-01', periods=15),
        'C': ['A', 'B', 'C'] * 5,
        'D': pd.Categorical(['A', 'B', 'C'] * 5)
    })
