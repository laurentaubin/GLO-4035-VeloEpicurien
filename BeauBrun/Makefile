run:
	python src/__main__.py

test:
	nosetests -v

format:
	black src; \
	black test; \
	black script; \
	black integration; \

check-format:
	black --check src
	black --check test

lint:
	pylint --rcfile=setup.cfg src --fail-under=9.5; \
	pylint --rcfile=setup.cfg test --disable="W0613" --fail-under=9.5;

clean:
	rm -rf .pytest_cache .coverage .pytest_cache coverage.xml