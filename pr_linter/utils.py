import os
import stat


def on_permission_error(func, path, exc_info):
    """Callback for shutil.rmtree() when a file is read-only. This causes an
    error on Windows in non-empty git repositories."""
    os.chmod(path, stat.S_IWRITE)
    os.unlink(path)
