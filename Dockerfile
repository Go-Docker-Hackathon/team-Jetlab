FROM    python:2
Add src/python/main /code
EXPOSE 5000
CMD ["python", "mshuang/shangweb.py"]
