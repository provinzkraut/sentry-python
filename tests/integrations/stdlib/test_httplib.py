try:
    from urllib.request import urlopen
except ImportError:
    from urllib import urlopen

from sentry_sdk import capture_message
from sentry_sdk.integrations.stdlib import StdlibIntegration


def test_crumb_capture(sentry_init, capture_events):
    sentry_init(integrations=[StdlibIntegration()])
    events = capture_events()

    url = "https://httpbin.org/status/200"
    response = urlopen(url)
    assert response.getcode() == 200
    capture_message("Testing!")

    event, = events
    crumb, = event["breadcrumbs"]
    assert crumb["type"] == "http"
    assert crumb["category"] == "httplib"
    assert crumb["data"] == {
        "url": url,
        "method": "GET",
        "status_code": 200,
        "reason": "OK",
    }