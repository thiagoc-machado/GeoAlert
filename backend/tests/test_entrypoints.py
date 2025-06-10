from manage import main

def test_manage_import(monkeypatch):
    import runpy
    import sys

    monkeypatch.setenv('DJANGO_SETTINGS_MODULE', 'geoalert.settings')
    original_argv = sys.argv
    sys.argv = ['manage.py', 'check']

    try:
        runpy.run_path('manage.py', run_name='__main__')
    finally:
        sys.argv = original_argv


def test_manage_main_function(monkeypatch):
    import sys
    monkeypatch.setattr(sys, 'argv', ['manage.py', 'check'])
    main()  # força entrada no if __name__ == '__main__'
