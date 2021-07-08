install:
	test -d venv || virtualenv venv -p python3.9
	. venv/bin/activate; pip install --upgrade pip
	. venv/bin/activate; pip install cython
	. venv/bin/activate; pip install -Ur requirements.txt

run: install
	. venv/bin/activate; uvicorn app.main:app --reload

clean:
	rm -r venv/