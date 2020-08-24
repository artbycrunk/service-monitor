import pytest
from service_monitor import summary


@pytest.mark.parametrize(
    "test, result",
    [
        (

            [
                summary.SummaryRow(
                    0,
                    "test",
                    "www.google.com",
                    ["200", "400", "400"],
                    [],

                )
            ],
            {
                "url": "www.google.com",
                "total_checks": 3,
                "passed_checks": 1,
                "failed_checks": 2,
                "failed_checks_percent": 67,
            },
        ),
        (
            [
               summary.SummaryRow(1, "zebra", "www.google.com", ["200"], []),
            ],
            {
                "url": "www.google.com",
                "total_checks": 1,
                "passed_checks": 1,
                "failed_checks": 0,
                "failed_checks_percent": 0,
            },
        ),
        (
            [
                summary.SummaryRow(
                    2,
                    "lion",
                    "www.google.com",
                    ["400", "400", "400"],
                    [],
                )
            ],
            {
                "url": "www.google.com",
                "total_checks": 3,
                "passed_checks": 0,
                "failed_checks": 3,
                "failed_checks_percent": 100,
            },
        ),
    ],
)
def test_stats(test, result):
    response = summary.get_stats(test)
    assert response[test[0].pos] == result
