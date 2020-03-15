
test:
	pytest \
		-vv --pep8 --flakes corus \
		--cov corus --cov-report term-missing --cov-report xml corus \
		--nbval --current-env docs.ipynb

version:
	bumpversion minor

wheel:
	python setup.py bdist_wheel

upload:
	twine upload dist/*

clean:
	find . \
		-name '*.pyc' \
		-o -name __pycache__ \
		-o -name .DS_Store \
		| xargs rm -rf

	rm -rf dist/ build/ .pytest_cache/ .cache/ .ipynb_checkpoints/ \
		*.egg-info/ coverage.xml .coverage
