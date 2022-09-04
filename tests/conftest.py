import pytest
from src.utils.api_factory import create_app
from src.conf.config import config_variables


@pytest.fixture(scope="module")
def app():
  '''
    Instance of main flask app
  '''
  return create_app(config_variables())
