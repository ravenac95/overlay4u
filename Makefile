# Install develop dependencies
develop:
	vstrap init

# Run all tests
test:
	nosetests -d

# Run medium and small tests only
medium-test:
	nosetests -a '!large' -d

# Run small tests only
small-test:
	nosetests -A 'not (medium or large)' -d

distribute:
	@python setup.py sdist upload
