FROM    python:2
run pip install pingpp
run pip install flask
run pip install pymongo
run pip install mongoengine
Add src/python/main /code
EXPOSE 5000
CMD ["python", "mshuang/shangweb.py"]
