
test:
	pytest -vv --pep8 --flakes corus --cov corus --cov-report term-missing --nbval docs.ipynb
