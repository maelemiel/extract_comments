try:
    from src.cli import main
except ImportError:
    # Fallback pour PyInstaller (src est dans le même dossier)
    from cli import main

if __name__ == "__main__":
    main()
