from pathlib import Path
import os
import tempfile

class TextEditor:

    MAX_FILE_SIZE = 10 * 1024 * 1024

    @staticmethod
    def open_file(path):
        path = Path(path)

        if not path.is_file():
            raise FileNotFoundError(path)

        if path.stat().st_size > TextEditor.MAX_FILE_SIZE:
            raise ValueError("File exceeds 10 MB limit")

        return path.read_text(encoding="utf-8")

    @staticmethod
    def save_file(path, content):
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)

        fd, temp_path = tempfile.mkstemp(
            prefix=".easyfm_",
            dir=str(path.parent)
        )

        try:
            with os.fdopen(fd, "w", encoding="utf-8") as file:
                file.write(content)
                file.flush()
                os.fsync(file.fileno())

            os.replace(temp_path, path)
        except Exception:
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            raise

        return str(path)

    @staticmethod
    def search(content, query):
        if not query:
            return []

        return [
            (index + 1, line)
            for index, line in enumerate(content.splitlines())
            if query.lower() in line.lower()
        ]

    @staticmethod
    def replace(content, old, new):
        if not old:
            raise ValueError("Search text cannot be empty")

        return content.replace(old, new)
