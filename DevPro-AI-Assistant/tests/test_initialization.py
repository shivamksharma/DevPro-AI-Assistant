import os
import pytest

def test_import_modules():
    """
    Tests that all core modules can be imported without raising an exception.
    """
    try:
        from devpro_ai_assistant.config import settings
        from devpro_ai_assistant.modules import speech_to_text
        from devpro_ai_assistant.modules import text_to_speech
        from devpro_ai_assistant.modules import command_handler
        from devpro_ai_assistant.modules import app_launcher
        from devpro_ai_assistant.modules import web_search
    except ImportError as e:
        pytest.fail(f"Failed to import one or more modules: {e}")

def test_settings_load():
    """
    Tests that the settings file can be loaded and contains the wake word.
    """
    from devpro_ai_assistant.config import settings
    assert hasattr(settings, 'WAKE_WORD')
    assert isinstance(settings.WAKE_WORD, str)

def test_main_script_compiles():
    """
    Tests that the __main__.py script is syntactically correct.
    This is a simple way to catch basic errors without running the full application.
    """
    # Construct a path to the __main__.py file relative to this test file.
    main_script_path = os.path.join(
        os.path.dirname(__file__), '..', 'devpro_ai_assistant', '__main__.py'
    )

    try:
        with open(main_script_path) as f:
            compile(f.read(), '__main__.py', 'exec')
    except SyntaxError as e:
        pytest.fail(f"__main__.py has a syntax error: {e}")
    except FileNotFoundError:
        pytest.fail(f"__main__.py not found at {main_script_path}")