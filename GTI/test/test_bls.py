import pytest
from GTI.data.bls import BLS

def test_bls():
    bls = BLS()
    data = bls.us_job_opening()
    assert data is not None
