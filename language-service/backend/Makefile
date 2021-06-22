install:
	virtualenv venv -p python3.8;
	. venv/bin/activate; 
	pip install -r requirements.txt; 

run: install
	uvicorn app.main:app --reload

clean:
	rm -r venv/