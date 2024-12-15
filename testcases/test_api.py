import pytest
import requests
import json
from common.request_util import RequestUtil
from common.yaml_util import YamlUtil
from test import Test
from common.parameterize_util import ddt,read_testcase

class TestRequest1:
    pass
    @pytest.mark.parametrize("caseinfo",read_testcase('get_api.yaml'))
    def test_get_api(self,caseinfo):
        RequestUtil("base_test_url",Test()).standard_yaml(caseinfo)



