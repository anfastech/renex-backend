 backend/
│   │   ├── app/
│   │   │   ├── __init__.py
│   │   │   ├── main.py
│   │   │   ├── database.py
│   │   │   └── routers.py
│   │   ├── env/
│   │   │   ├── include
│   │   │   ├── Lib
│   │   │   ├── scripts
│   │   │   └── pyvenv.cfg
│   │   ├── .env
│   │   ├── requirements.txt


Method : 
|  virtual environment env/ activation  |  running uvicorn

* env\Scripts\activate    
-> http://127.0.0.1:8000/
* uvicorn app.main:app --reload
-> http://127.0.0.1:8000

renex/
│
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── database.py
│   │   └── routers.py
│   ├── env/
│   │   ├── include
│   │   ├── Lib
│   │   ├── scripts
│   │   └── pyvenv.cfg
│   ├── .env
│   ├── settings.py
│   └── requirements.txt