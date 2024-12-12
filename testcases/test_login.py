import pytest
import requests
import json
from common.request_util import RequestUtil
from common.yaml_util import YamlUtil
from test import Test
from common.parameterize_util import ddt,read_testcase

class TestRequest:
    pass
    @pytest.mark.parametrize("caseinfo",read_testcase('get_token.yaml'))
    def test_login(self,caseinfo):
        RequestUtil("base_test_url",Test()).standard_yaml(caseinfo)

    @pytest.mark.parametrize("caseinfo", read_testcase('userinfo.yaml'))
    def test_userinfo(self, caseinfo):
        RequestUtil("base_test_url", Test()).standard_yaml(caseinfo)

    @pytest.mark.parametrize("caseinfo", read_testcase('city_type.yaml'))
    def test_city(self, caseinfo):
       RequestUtil("base_test_url",Test()).standard_yaml(caseinfo)
    #
    @pytest.mark.parametrize("caseinfo", read_testcase('mapid.yaml'))
    def test_mapid(self, caseinfo):
        RequestUtil("base_test_url", Test()).standard_yaml(caseinfo)

    @pytest.mark.parametrize("caseinfo", read_testcase('simulation.yaml'))
    def test_simulation(self, caseinfo):
        RequestUtil("base_test_url",Test()).standard_yaml(caseinfo)

    @pytest.mark.parametrize("caseinfo", read_testcase('ranAsPlan.yaml'))
    def test_ranAsPlan(self, caseinfo):
        RequestUtil("base_test_url",Test()).standard_yaml(caseinfo)
