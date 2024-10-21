pyright: 
  poetry run pyright .

ruff: 
  poetry run ruff check . --fix && poetry run ruff format .

req: 
  poetry export -f requirements.txt --output requirements.txt --without-hashes
