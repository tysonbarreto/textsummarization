from dataclasses import dataclass, field
from pathlib import Path

@dataclass(frozen=True)
class DataIngestionConfig:
    root_dir: Path
    source_dir: Path
    file_name: str


if __name__=="__main__":
    __all__=["DataIngestionConfig"]