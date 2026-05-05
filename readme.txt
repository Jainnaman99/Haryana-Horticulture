project/
│
├── main.py                     # App entry point
├── config/
│   ├── __init__.py
│   └── settings.py              # Environment variables & app settings
│
├── domain/                      # Core business rules (entities, interfaces)
│   ├── __init__.py
│   ├── entities/
│   │   ├── __init__.py
│   │   ├── user.py              # User entity
│   │   └── product.py           # Product entity
│   ├── interfaces/
│   │   ├── __init__.py
│   │   ├── user_repository.py   # Abstract repository interface for users
│   │   └── product_repository.py
│   └── exceptions.py            # Domain-specific exceptions
│
├── persistence/                 # Data access layer (repositories, queries)
│   ├── __init__.py
│   ├── repositories  # Implements domain interfaces 
│  
│
├── application/                 # Business logic / use cases
│   ├── __init__.py
│   └── services/
│       ├── __init__.py
│       ├── user_service.py      # Business rules for users
│       └── product_service.py   # Business rules for products
│
├── presentation/                # API layer (routers, request/response handling)
│   ├── __init__.py
│   └── api/
│       ├── __init__.py
│       └── v1/
│           ├── __init__.py
│           ├── sample.py        # Example router
│           ├── users.py         # Users router
│           └── products.py      # Products router
│
├── infrastructure/              # Low-level technical details (DB, external APIs)
│   ├── __init__.py
│   └── database/
│       ├── __init__.py
│       ├── connection.py        # init_db(), async_engine, session creation
│       └── models.py            # SQLAlchemy ORM models
│
├── requirements.txt             # Dependencies
└── README.md
Application->Dependencies->Folder->Files(with DI code)
OR
Repo->its own DI
Service->its own DI




project/
│
├── main.py                     
├── config/
│   ├── __init__.py
│   └── settings.py              
│
├── domain/                      
│   ├── __init__.py
│   ├── entities/
│   │   ├── __init__.py
│   │   ├── user.py              
│   │   └── product.py           
│   ├── interfaces/
│   │   ├── __init__.py
│   │   ├── user_repository.py   
│   │   └── product_repository.py
│   └── exceptions.py            
│
├── persistence/                 
│   ├── __init__.py
│   ├── repositories             
│  
├── application/                 
│   ├── __init__.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── user_service.py      
│   │   └── product_service.py   
│   └── dependencies/            # ⬅️ New folder for DI
│       ├── __init__.py
│       ├── users/               # Dependencies specific to Users
│       │   ├── __init__.py
│       │   └── user_dependencies.py
│       ├── products/            # Dependencies specific to Products
│       │   ├── __init__.py
│       │   └── product_dependencies.py
│       └── common.py            # Shared DI (like db_session, logger, etc.)
│
├── presentation/                
│   ├── __init__.py
│   └── api/
│       ├── __init__.py
│       └── v1/
│           ├── __init__.py
│           ├── sample.py        
│           ├── users.py         
│           └── products.py      
│
├── infrastructure/              
│   ├── __init__.py
│   └── database/
│       ├── __init__.py
│       ├── connection.py        
│       └── models.py            
│
├── requirements.txt             
└── README.md


Steps to run the project (Windows PowerShell)

Open PowerShell and go to the project folder
cd C:\project\Horticulture\Horticulture-API
Create and activate a virtual environment
python -m venv .venv
If activation is blocked: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
..venv\Scripts\Activate.ps1
Install dependencies
python -m pip install --upgrade pip
pip install -r requirements.txt
Install ODBC driver (required by your DB connection)
Install "ODBC Driver 18 for SQL Server" from Microsoft (required for the connection string in connection.py).
If pip fails building DB drivers (pyodbc/aioodbc), install Microsoft Build Tools or use prebuilt wheels.
Run the app
From the project root run either:
python -m uvicorn main:app --host 127.0.0.1 --port 8080 --reload
or python main.py
Open Swagger UI at http://127.0.0.1:8080/docs