setup:
	virtualenv -p python3 .venv
	.venv/bin/pip install -r requirements.txt

clean:
	rm -fr .venv
