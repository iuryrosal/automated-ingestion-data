from unittest.mock import patch, call

from src.data.database import Database
from src.conf.config import config_variables

conn_str_expected = "sqlite://"


@patch.object(Database, 'create_engine_db')
def test_conn(mock_create_engine_db):
    expected_calls = [call(conn_str_expected),
                      call().connect(),
                      call(conn_str_expected),
                      call().connect()]

    Database(config_variables())

    mock_create_engine_db.assert_has_calls(expected_calls)


@patch.object(Database, 'connect_db')
def test_build_conn_str(mock_connect_db):
    database = Database(config_variables())
    conn_str = database.build_conn_str()

    assert conn_str_expected == conn_str
