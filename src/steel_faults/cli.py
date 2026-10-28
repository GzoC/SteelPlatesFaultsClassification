import argparse
import subprocess
import sys
from pathlib import Path

from .training import train


def main():
    parser = argparse.ArgumentParser(description="Steel defect classification study")
    commands = parser.add_subparsers(dest="command", required=True)
    fit = commands.add_parser("train")
    fit.add_argument("--data", type=Path, default=Path("data/raw/Faults.NNA"))
    fit.add_argument("--output", type=Path, default=Path("var/model"))
    ui = commands.add_parser("dashboard")
    ui.add_argument("--port", type=int, default=8501)
    args = parser.parse_args()
    if args.command == "train":
        result = train(args.data, args.output)
        print(
            f"Selected: {result['selected']}; test macro-F1: {result['test'][result['selected']]['macro_f1']:.4f}"
        )
    else:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                str(Path(__file__).with_name("dashboard.py")),
                "--server.address=127.0.0.1",
                f"--server.port={args.port}",
                "--server.headless=true",
            ],
            check=True,
        )


if __name__ == "__main__":
    main()
