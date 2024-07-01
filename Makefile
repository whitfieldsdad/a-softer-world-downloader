build:
	poetry build

release: build
	poetry publish

requirements:
	poetry export -f requirements.txt --output requirements.txt --without-hashes
