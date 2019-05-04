
test:
	pytest -vv --pep8 --flakes corus --cov corus --cov-report term-missing --nbval docs.ipynb

ci:
	pytest -vv --pep8 --flakes corus --cov corus --cov-report xml --nbval docs.ipynb

wheel:
	python setup.py bdist_wheel

upload:
	twine upload dist/*

clean:
	find corus -name '*.pyc' -not -path '*/__pycache__/*' -o -name '.DS_Store*' | xargs rm
	rm -rf dist build *.egg-info coverage.xml
