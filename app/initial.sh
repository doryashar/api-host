# cd build
# python -m pytest app/tests
# aerich upgrade
python app/initial_data.py

uvicorn app.main:app --host 0.0.0.0 --port 80