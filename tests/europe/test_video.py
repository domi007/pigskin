import pytest
import vcr

from pigskin.pigskin import pigskin


@pytest.fixture(scope='class')
def gp():
    with vcr.use_cassette('backends/europe/gp.yaml'):
        return pigskin()


@pytest.mark.incremental
class TestEuropeVideo(object):
    """These don't require authentication to Game Pass."""
    @vcr.use_cassette('backends/europe/video__get_diva_config.yaml')
    @staticmethod
    def test__get_diva_config(gp):
        diva_config_url = gp._store.gp_config['modules']['DIVA']['HTML5']['SETTINGS']['Live24x7']

        diva_config = gp._video._get_diva_config(diva_config_url)

        # check the response
        assert diva_config
        assert diva_config['processing_url']
        assert diva_config['video_data_url']


@pytest.mark.incremental
class TestEuropeVideoAuth(object):
    """These require authentication to Game Pass"""
    @vcr.use_cassette('backends/europe/video_auth_login.yaml')
    @staticmethod
    def test_login(gp):
        assert gp.login(pytest.gp_username, pytest.gp_password, force=True)

        # make sure tokens are actually set
        assert gp._store.access_token
        assert gp._store.refresh_token


    @staticmethod
    def test__build_processing_url_payload(gp):
        video_id = 'this_is_a_video_id'
        vs_url = 'https://this.is.a.video.source.url'

        response = gp._video._build_processing_url_payload(video_id, vs_url)

        assert response
        for i in [video_id, vs_url, gp._store.access_token]:
            assert i in response
