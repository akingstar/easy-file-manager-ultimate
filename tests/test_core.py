import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import tempfile
import zipfile
from pathlib import Path

from core.file_operations import FileOperations
from core.archive_manager import ArchiveManager
from core.text_editor import TextEditor
from core.hex_editor import HexEditor
from core.database import Database
from core.apk_inspector import APKInspector

def run_tests():
    with tempfile.TemporaryDirectory() as tmp:
        base = Path(tmp)
        source = base / "hello.txt"
        source.write_text("Easy File Manager")

        # File operations
        assert FileOperations.list_files(tmp)
        FileOperations.copy(source, base / "copy.txt")
        assert (base / "copy.txt").exists()

        # Rename
        FileOperations.rename(base / "copy.txt", "renamed.txt")
        assert (base / "renamed.txt").exists()

        # Text editor
        assert TextEditor.open_file(source) == "Easy File Manager"
        TextEditor.save_file(source, "Updated")
        assert TextEditor.open_file(source) == "Updated"

        # HEX editor
        HexEditor.write_bytes(source, 0, b"TEST")
        assert HexEditor.read(source, 0, 4) == b"TEST"

        # Archive manager
        archive = base / "test.zip"
        ArchiveManager.create_zip(source, archive)
        assert "hello.txt" in ArchiveManager.list_archive(archive)

        extracted = base / "extracted"
        ArchiveManager.extract(archive, extracted)
        assert (extracted / "hello.txt").exists()

        # APK inspector structure test
        apk = base / "sample.apk"
        with zipfile.ZipFile(apk, "w") as z:
            z.writestr("AndroidManifest.xml", "test")
            z.writestr("classes.dex", "test")

        info = APKInspector.inspect(apk)
        assert info["manifest"] is True
        assert "classes.dex" in info["dex_files"]

        # Database
        db = Database(base / "test.db")
        db.add_bookmark("Home", "/storage/emulated/0")
        assert db.get_bookmarks()[0][0] == "Home"

    print("ALL CORE TESTS PASSED")

if __name__ == "__main__":
    run_tests()
