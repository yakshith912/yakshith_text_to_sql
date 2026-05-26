from pathlib import Path


def main() -> None:
    app_path = Path(__file__).resolve().parent / "app.py"
    content = app_path.read_text(encoding="utf-8")
    content = content.replace('use_container_width=True', "width='stretch'")
    content = content.replace('use_container_width=False', "width='content'")
    app_path.write_text(content, encoding="utf-8")
    print("Done")


if __name__ == "__main__":
    main()
