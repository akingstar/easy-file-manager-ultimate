import zipfile
import tarfile
from pathlib import Path

class ArchiveManager:

    @staticmethod
    def list_archive(path):
        path = Path(path)

        if zipfile.is_zipfile(path):
            with zipfile.ZipFile(path) as archive:
                return archive.namelist()

        if tarfile.is_tarfile(path):
            with tarfile.open(path) as archive:
                return archive.getnames()

        raise ValueError("Unsupported archive format")

    @staticmethod
    def create_zip(source, destination):
        source = Path(source)
        destination = Path(destination)

        with zipfile.ZipFile(
            destination, "w", zipfile.ZIP_DEFLATED
        ) as archive:
            if source.is_file():
                archive.write(source, source.name)
            else:
                for item in source.rglob("*"):
                    if item.is_file():
                        archive.write(
                            item, item.relative_to(source.parent)
                        )

        return str(destination)

    @staticmethod
    def extract(path, destination):
        path = Path(path)
        destination = Path(destination).resolve()
        destination.mkdir(parents=True, exist_ok=True)

        def safe_target(name):
            target = (destination / name).resolve()
            if not target.is_relative_to(destination):
                raise ValueError("Unsafe archive path detected")
            return target

        if zipfile.is_zipfile(path):
            with zipfile.ZipFile(path) as archive:
                for item in archive.infolist():
                    safe_target(item.filename)
                archive.extractall(destination)
        elif tarfile.is_tarfile(path):
            with tarfile.open(path) as archive:
                for item in archive.getmembers():
                    safe_target(item.name)
                    if item.issym() or item.islnk():
                        raise ValueError("Archive links are not supported")
                archive.extractall(destination, filter="data")
        else:
            raise ValueError("Unsupported archive format")

        return str(destination)
