from geoalert.celery import app

def test_celery_app_import():
    assert app.main == 'geoalert'

def test_celery_app_config():
    assert isinstance(app.conf.task_default_queue, str)
