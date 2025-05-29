# Example usage of Extract Comments

This folder contains a sample project to demonstrate the features of `extract_comments.py`.

## Project structure

- `app.py`: Sample Python application
- `script.js`: JavaScript file with various annotations
- `styles.css`: CSS file for styling
- `index.html`: Simple HTML page

## Annotation types present

- TODO
- FIXME
- BUG
- HACK
- NOTE
- OPTIMIZE
- REVIEW
- QUESTION
- IDEA

## How to run extraction on this example

To analyze only this example directory, run the following command:

```bash
cd ..
python3 extract_comments.py --directory ./examples --output ./examples/rapport.md --json-output ./examples/rapport.json --simple
```

Or

```bash
chmod +x extract_comments.py
./extract_comments.py --directory ./examples --output ./examples/rapport.md --json-output ./examples/rapport.json --simple
```

Or

```bash
chmod +x run_example.sh
./run_example.sh
```

This will generate:

- `./examples/rapport.md` - Simplified report
- `./examples/rapport_detailed.md` - Detailed report
- `./examples/rapport.json` - Data in JSON format
