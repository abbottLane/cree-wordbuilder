install:
	virtualenv -p python3.7 venv;
	. venv/bin/activate; 
	pip install -r requirements.txt; 

run: install
	uvicorn app.main:app --reload

clean:
	rm -r venv/