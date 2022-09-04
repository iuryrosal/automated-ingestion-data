from src.conf.config import config_variables
from unittest.mock import patch

# Local environment
env = {
    "POSTGRES_USER": "root",
    "POSTGRES_PASSWORD": "password",
    "POSTGRES_HOST": "localhost",
    "POSTGRES_PORT": 5432,
    "POSTGRES_DB": "data_vehicles",
    "CONN_STR": "sqlite://",
    "CONNECTION": "conn",
    "ENGINE": "engine",
    "ENV": "local"
}


def get_conn_att():
    return {
        "CONN_STR": "sqlite://",
        "CONNECTION": "conn",
        "ENGINE": "engine"
    }


@patch("src.data.database.Database.get_conn_att")
def test_config_local_env(mock_get_conn_att):
    mock_get_conn_att.return_value = get_conn_att()
    config = config_variables()
    config_dict_expected = env
    assert config_dict_expected == config
