
import pytest


@pytest.fixture(scope="function")
def pass_capsys(request, capsys):
    request.cls.capsys = capsys
