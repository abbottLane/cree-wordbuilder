install:
	test -d venv || virtualenv venv -p python3.7
	. venv/bin/activate; pip install --upgrade pip
	. venv/bin/activate; pip install -Ur requirements.txt

run: install
	uvicorn app.main:app --reload

clean:
	rm -r venv/