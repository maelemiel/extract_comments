NAME = extract_comments
SRC = __main__.py

run:
	python3 -m $(SRC) $(ARGS)

build:
	pyinstaller --onefile -n $(NAME) $(SRC)

clean:
	rm -rf build dist __pycache__ *.spec

.PHONY: run build clean