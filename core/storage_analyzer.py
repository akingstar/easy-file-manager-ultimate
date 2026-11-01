import os
import shutil
import hashlib
from pathlib import Path
from collections import defaultdict

class StorageAnalyzer:

    @staticmethod
    def storage_info(path):
        usage = shutil.disk_usage(path)
        return {
            "total": usage.total,
            "used": usage.used,
            "free": usage.free,
            "used_percent": round(usage.used * 100 / usage.total, 2)
        }

    @staticmethod
    def largest_files(path, limit=20):
        results = []

        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if not os.path.islink(
                os.path.join(root, d)
            )]

            for name in files:
                full_path = os.path.join(root, name)
                try:
                    if not os.path.islink(full_path):
                        results.append(
                            (full_path, os.path.getsize(full_path))
                        )
                except OSError:
                    continue

        return sorted(results, key=lambda x: x[1], reverse=True)[:limit]

    @staticmethod
    def duplicate_files(path):
        groups = defaultdict(list)

        for root, dirs, files in os.walk(path):
            dirs[:] = [d for d in dirs if not os.path.islink(
                os.path.join(root, d)
            )]

            for name in files:
                full_path = os.path.join(root, name)

                try:
                    if os.path.islink(full_path):
                        continue

                    size = os.path.getsize(full_path)
                    if size == 0:
                        continue

                    groups[size].append(full_path)
                except OSError:
                    continue

        duplicates = []

        for paths in groups.values():
            if len(paths) < 2:
                continue

            hashes = defaultdict(list)

            for file_path in paths:
                try:
                    digest = hashlib.sha256()
                    with open(file_path, "rb") as file:
                        for chunk in iter(
                            lambda: file.read(1024 * 1024), b""
                        ):
                            digest.update(chunk)

                    hashes[digest.hexdigest()].append(file_path)
                except OSError:
                    continue

            duplicates.extend(
                group for group in hashes.values() if len(group) > 1
            )

        return duplicates
