import zipfile
import hashlib
from pathlib import Path

class APKInspector:

    @staticmethod
    def inspect(apk_path):
        apk = Path(apk_path)

        if not zipfile.is_zipfile(apk):
            raise ValueError("Invalid APK file")

        result = {
            "filename": apk.name,
            "size": apk.stat().st_size,
            "sha256": "",
            "manifest": False,
            "dex_files": [],
            "native_architectures": [],
            "resources": [],
            "signatures": [],
            "other_files": []
        }

        digest = hashlib.sha256()
        with open(apk, "rb") as file:
            for chunk in iter(lambda: file.read(1024 * 1024), b""):
                digest.update(chunk)
        result["sha256"] = digest.hexdigest()

        with zipfile.ZipFile(apk) as archive:
            for item in archive.infolist():
                name = item.filename

                if name == "AndroidManifest.xml":
                    result["manifest"] = True
                elif name.endswith(".dex"):
                    result["dex_files"].append(name)
                elif name.startswith("lib/"):
                    parts = name.split("/")
                    if len(parts) > 2:
                        result["native_architectures"].append(parts[1])
                elif name.startswith("res/"):
                    result["resources"].append(name)
                elif name.startswith("META-INF/"):
                    result["signatures"].append(name)
                else:
                    result["other_files"].append(name)

        result["native_architectures"] = sorted(
            set(result["native_architectures"])
        )
        return result

    @staticmethod
    def list_contents(apk_path):
        with zipfile.ZipFile(apk_path) as archive:
            return archive.namelist()
