
test:
	pytest -vv --pep8 --flakes corus --cov corus --cov-report term-missing --nbval --current-env docs.ipynb

ci:
	pytest -vv --pep8 --flakes corus --cov corus --cov-report xml --nbval-lax --current-env docs.ipynb

wheel:
	python setup.py bdist_wheel

upload:
	twine upload dist/*

clean:
	find corus -name '*.pyc' -not -path '*/__pycache__/*' -o -name '.DS_Store*' | xargs rm
	rm -rf dist build *.egg-info coverage.xml
