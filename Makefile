.PHONY: setup
setup: clean
	virtualenv -p python3 .venv
	.venv/bin/pip install -r requirements.txt
	@echo "\nTo use environment: source .venv/bin/activate"

.PHONY: clean
clean:
	rm -fr .venv
	find . -iname __pycache__ | xargs rm -fr

.PHONY: install
install: uninstall
	ln -s "`pwd`/slacker.sh" /usr/local/bin/slacker

.PHONY: uninstall
uninstall:
	rm -f /usr/local/bin/slacker

.PHONY: update-requirements
update-requirements: setup
	.venv/bin/pip freeze > requirements.txt

.PHONY: check-cmds
check-cmds:
	./slacker.py --verbose --check

.PHONY: check-style
check-style:
	.venv/bin/flake8 --ignore E111,E114,E121,E126,E302 --max-line-length 100 --count --show-source \
	  slacker slacker.py

.PHONY: static-analysis
static-analysis:
	.venv/bin/vulture --min-confidence 60 --sort-by-size --exclude slacker/commands/__init__.py \
	  slacker slacker.py .vulture_whitelist.py

.PHONY: check-min-version
check-min-version:
	.venv/bin/vermin -t 3.4 slacker slacker.py

.PHONY: check
check: check-min-version check-cmds check-style static-analysis

.PHONY: docker
docker:
	docker build -t slacker:local .
