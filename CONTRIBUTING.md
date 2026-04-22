# Contributing

## How To Contribute

1. Fork the repository.
2. Create a feature branch from `main`.
3. Make your changes with clear commit messages.
4. Run local checks before opening a pull request.
5. Open a pull request with a concise summary and test notes.

## Local Checks

Use your project virtual environment and run:

```bash
python -m compileall src
```

If you add new modules, ensure imports are valid and the app still launches with:

```bash
python main.py
```

## Pull Request Guidelines

- Keep changes focused and minimal.
- Update `README.md` or `Doc.md` when behavior changes.
- Add an entry to `CHANGELOG.md` under `Unreleased`.
- Do not commit local runtime artifacts (`.venv`, logs, output files, local settings).
