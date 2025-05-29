NAME = extract_comments
SRC = __main__.py

run:
	python3 $(SRC) $(ARGS)

build:
    pyinstaller --onefile -n $(NAME) --add-data "src/report_html.py:." $(SRC)
	@cp dist/$(NAME) ../$(NAME)	@cp dist/$(NAME) ../$(NAME)

clean:
	rm -rf build dist __pycache__ *.spec

.PHONY: run build clean
