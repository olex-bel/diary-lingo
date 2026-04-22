import pathlib
from datetime import datetime
from typing import List

class FileService:
    def __init__(self, directory: str) -> None:
        self.root: pathlib.Path = pathlib.Path(directory)
        self.root.mkdir(parents=True, exist_ok=True)
        
    def get_files(self) -> List[str]:
        try:
            sorted_files = sorted([f for f in self.root.glob("*") if f.is_file()], key=lambda x: x.stat().st_mtime, reverse=True)
            return [f.name for f in sorted_files]
        except Exception:           
            return []

    def read_file_content(self, filename: str) -> str:
        file_path = self.root / filename
        return file_path.read_text(encoding="utf-8")

    def get_full_path(self, filename: str) -> str:
        return str(self.root / filename)
    
    def generate_unique_filename(self, prefix: str = "note", extension: str = "txt") -> str:
        date_str = datetime.now().strftime("%Y-%m-%d")
        base_name = f"{prefix}_{date_str}"
        
        counter = 1
        filename = f"{base_name}_{counter}.{extension}"
        
        while (self.root / filename).exists():
            counter += 1
            filename = f"{base_name}_{counter}.{extension}"
            
        return filename