# Create your tests here.
import pytest

from isfahan.market.management.commands.yahoo_sp500_bulk import Command


@pytest.mark.django_db()
def test_yfinance():
    """
    add parameters to limit data
    validate that the update was successful

    """
    command = Command().handle()

    assert command == "this test is not complete but I want the linter to shut up"
