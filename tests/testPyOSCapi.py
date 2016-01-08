import requests
import responses
import random
import simplejson as json

from pyOSCapi import OSCAPI as OSC
from nose.tools import assert_is_not_none

class TestOSC(object):
    @responses.activate
    def test_connect(self):
        def request_callback(request):
            resp_body = {'state':'done', 'results':{'sessionId': random.randint(1,256)}}
            headers = {'content-type':'application/json'}
            return (200, headers, json.dumps(resp_body))

        responses.add_callback(responses.POST,
            'http://oscapi.test:8080/osc/commands/execute',
            callback=request_callback,
            content_type='application/json'
            )
        cam = OSC("oscapi.test", "8080")
        resp = cam.connect()
        assert_is_not_none(resp)
        assert_is_not_none(cam.getSid())

if __name__ == '__main__':
    unittest.main()
