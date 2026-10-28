from pathlib import Path

import nbformat
from nbclient import NotebookClient

root = Path(__file__).resolve().parents[1]
notebook = nbformat.read(root / "notebooks/01_reproducible_study.ipynb", as_version=4)
NotebookClient(
    notebook, timeout=180, kernel_name="python3", resources={"metadata": {"path": str(root)}}
).execute()
destination = root / "var/executed-study.ipynb"
destination.parent.mkdir(exist_ok=True)
nbformat.write(notebook, destination)
print(destination)
