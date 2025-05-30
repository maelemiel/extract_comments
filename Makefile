NAME = extract_comments
SRC = __main__.py

run:
	pyinstaller --onefile -n extract_comments --add-data "src/report_html.py:." __main__.py
	@cp dist/$(NAME) ../$(NAME)

clean:
	rm -rf build dist __pycache__ *.spec

.PHONY: run clean
