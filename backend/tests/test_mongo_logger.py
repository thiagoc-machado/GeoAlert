# tests/test_mongo_logger.py

import pytest
from core import mongo_logger
from unittest.mock import patch
from core.mongo_logger import log_ia_action


def test_log_ia_action(monkeypatch):
    class FakeCollection:
        def insert_one(self, data):
            assert data['user_id'] == 1
            assert data['type'] == 'summary'
            assert 'input' in data and 'result' in data
            return True

    class FakeDB:
        def __getitem__(self, name):
            return FakeCollection()

    class FakeClient:
        def __getitem__(self, name):
            return FakeDB()

    monkeypatch.setattr(mongo_logger, 'client', FakeClient())
    mongo_logger.log_ia_action(
        user_id=1,
        action_type='summary',
        input_data={'text': 'Exemplo'},
        result_data={'summary': 'Resumo gerado'}
    )

@patch('core.mongo_logger.collection.insert_one')
def test_log_ia_action_success(mock_insert):
    log_ia_action(
        user_id=1,
        action_type='test',
        input_data={'msg': 'entrada'},
        result_data={'msg': 'saida'}
    )
    mock_insert.assert_called_once()

@patch('core.mongo_logger.collection.insert_one', side_effect=Exception('Erro'))
def test_log_ia_action_exception(mock_insert):
    try:
        log_ia_action(
            user_id=1,
            action_type='fail',
            input_data={},
            result_data={}
        )
    except Exception:
        assert False
    assert True

@patch('core.mongo_logger.collection')
def test_log_ia_action_data(mock_collection):
    from core.mongo_logger import log_ia_action
    log_ia_action(2, 'test-type', {'msg': 'input'}, {'msg': 'result'})
    args, kwargs = mock_collection.insert_one.call_args
    assert 'user_id' in args[0]
    assert 'timestamp' in args[0]