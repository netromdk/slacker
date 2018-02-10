setup: clean
	virtualenv -p python3 .venv
	.venv/bin/pip install -r requirements.txt
	echo "\nTo use environment: source .venv/bin/activate"

clean:
	rm -fr .venv
	find . -iname __pycache__ | xargs rm -fr

install: uninstall
	ln -s "`pwd`/slacker.sh" /usr/local/bin/slacker

uninstall:
	rm -f /usr/local/bin/slacker
