import pytest
from GTI.auth_sync import AuthSync

def test_auth_sync():
    sync = AuthSync()
    sync.sync()
    assert True  # If no exceptions are raised, the test passes
