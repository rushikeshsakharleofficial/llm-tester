.PHONY: test check validate detect

test:
	python3 -m unittest discover -s tests

check:
	python3 -m compileall scripts tests
	python3 scripts/validate_skill.py .

detect:
	python3 scripts/detect_test_commands.py .

validate: check test detect
