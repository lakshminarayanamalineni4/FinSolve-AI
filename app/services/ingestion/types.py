from dataclasses import dataclass

# represents the raw loaded document.
@dataclass
class LoadedDocument:
    name: str
    source_path: str
    content: str

# LoadedDocument(
#     name="financial_summary.md",
#     source_path="resources/data/finance/financial_summary.md",
#     content="..."
# )

@dataclass
class NormalizedDocument:
    name: str
    source_path: str
    content: str
    file_type: str # md or csv
    department: str
    required_permission: str