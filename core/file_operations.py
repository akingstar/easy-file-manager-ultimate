import os
import shutil
import hashlib
from pathlib import Path

class FileOperations:

    @staticmethod
    def list_files(path):
        folder = Path(path)
        if not folder.is_dir():
            raise NotADirectoryError(path)

        return sorted(
            folder.iterdir(),
            key=lambda p: (not p.is_dir(), p.name.lower())
        )

    @staticmethod
    def create_folder(path, name):
        target = Path(path) / name
        target.mkdir(parents=False, exist_ok=False)
        return str(target)

    @staticmethod
    def rename(source, new_name):
        source = Path(source)
        target = source.with_name(new_name)
        if target.exists():
            raise FileExistsError(target)
        return str(source.rename(target))

    @staticmethod
    def copy(source, destination):
        source = Path(source)
        destination = Path(destination)

        if source.is_dir():
            shutil.copytree(source, destination)
        else:
            shutil.copy2(source, destination)

        return str(destination)

    @staticmethod
    def move(source, destination):
        return shutil.move(str(source), str(destination))

    @staticmethod
    def delete(path):
        target = Path(path)

        if target.is_symlink() or target.is_file():
            target.unlink()
        elif target.is_dir():
            shutil.rmtree(target)
        else:
            raise FileNotFoundError(path)

    @staticmethod
    def search(path, query):
        results = []
        for root, dirs, files in os.walk(path):
            for name in dirs + files:
                if query.lower() in name.lower():
                    results.append(str(Path(root) / name))
        return results

    @staticmethod
    def file_hash(path, algorithm="sha256"):
        digest = hashlib.new(algorithm)
        with open(path, "rb") as file:
            for chunk in iter(lambda: file.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()

    @staticmethod
    def storage_info(path):
        usage = shutil.disk_usage(path)
        return {
            "total": usage.total,
            "used": usage.used,
            "free": usage.free
        }
