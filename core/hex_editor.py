from pathlib import Path

class HexEditor:

    MAX_SIZE = 50 * 1024 * 1024

    @staticmethod
    def read(path, offset=0, length=256):
        path = Path(path)

        if not path.is_file():
            raise FileNotFoundError(path)

        if offset < 0 or length < 0:
            raise ValueError("Invalid offset or length")

        if offset > path.stat().st_size:
            raise ValueError("Offset exceeds file size")

        if path.stat().st_size > HexEditor.MAX_SIZE:
            raise ValueError("File exceeds 50 MB limit")

        with open(path, "rb") as file:
            file.seek(offset)
            return file.read(length)

    @staticmethod
    def format_hex(data, offset=0):
        lines = []

        for i in range(0, len(data), 16):
            chunk = data[i:i + 16]
            hex_part = " ".join(f"{b:02X}" for b in chunk)
            text_part = "".join(
                chr(b) if 32 <= b <= 126 else "."
                for b in chunk
            )

            lines.append(
                f"{offset + i:08X}  {hex_part:<47}  {text_part}"
            )

        return "\n".join(lines)

    @staticmethod
    def write_bytes(path, offset, data):
        path = Path(path)

        if not path.is_file():
            raise FileNotFoundError(path)

        if path.stat().st_size > HexEditor.MAX_SIZE:
            raise ValueError("File exceeds 50 MB limit")

        if offset < 0 or offset + len(data) > path.stat().st_size:
            raise ValueError("Write range exceeds file size")

        with open(path, "r+b") as file:
            file.seek(offset)
            file.write(data)
            file.flush()

        return True
