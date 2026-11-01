import subprocess
import shlex
import os

class RootManager:

    @staticmethod
    def is_root_available():
        try:
            result = subprocess.run(
                ["su", "-c", "id"],
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode == 0 and "uid=0" in result.stdout
        except (OSError, subprocess.TimeoutExpired):
            return False

    @staticmethod
    def execute(command, timeout=30):
        if not isinstance(command, list) or not command:
            raise ValueError("Invalid command")

        result = subprocess.run(
            ["su", "-c", shlex.join(command)],
            capture_output=True,
            text=True,
            timeout=timeout
        )

        if result.returncode != 0:
            raise RuntimeError(result.stderr.strip() or "Root command failed")

        return result.stdout

    @staticmethod
    def list_directory(path):
        return RootManager.execute(["ls", "-la", path])

    @staticmethod
    def change_permissions(path, mode):
        if not isinstance(mode, str) or not mode.isdigit():
            raise ValueError("Invalid permission mode")

        if len(mode) not in (3, 4):
            raise ValueError("Use a 3 or 4 digit permission mode")

        return RootManager.execute(["chmod", mode, path])

    @staticmethod
    def copy_file(source, destination):
        return RootManager.execute(["cp", "-a", source, destination])

    @staticmethod
    def move_file(source, destination):
        return RootManager.execute(["mv", source, destination])
