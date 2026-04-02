# 💰 Finance Tracking System

A RESTful API backend for managing personal finances with role-based access control, built with FastAPI and SQLite.

## ✨ Features

### Core Features
- **User Authentication** - Register and login with JWT tokens
- **Transaction Management** - Create, read, update, delete financial records
- **Filtering** - Filter transactions by date, category, and type
- **Financial Analytics** - Get summaries, category breakdowns, and monthly trends
- **Role-Based Access** - Different permissions for Viewer, Analyst, and Admin roles
- **Input Validation** - All inputs validated with meaningful error messages
- **API Documentation** - Auto-generated Swagger UI documentation

### Optional Features
- 📊 Category-wise spending analysis with percentages
- 📈 Monthly income/expense trends
- 🔍 Filter transactions with multiple criteria
- 💾 SQLite database persistence

## 🛠️ Tech Stack

| Technology           | Purpose |
|------------    |      ---------|
| **FastAPI**    |     Web framework for building APIs |
| **SQLAlchemy** |     SQL ORM for database operations |
| **SQLite**     |     Lightweight database |
| **Pydantic**   |     Data validation and serialization |
| **JWT**        |     Token-based authentication |
| **Uvicorn**    |     ASGI server |

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

#### 1. Clone the repository
in ```bash
git clone https://github.com/YOUR_USERNAME/finance-tracker.git
cd finance-tracker

#### 2. Create virtual environment
 Windows
python -m venv venv
venv\Scripts\activate

 Mac/Linux
python3 -m venv venv
source venv/bin/activate

#### 3. Install dependencies

pip install -r requirements.txt

#### 4. Set up environment variables

Copy example environment file
cp .env.example .env

Edit .env file (optional - defaults work)

DATABASE_URL=sqlite:///./finance_tracker.db
#ECRET_KEY=your-secret-key-here

#### 5. Run the application

uvicorn app.main_simple:app --reload

#### Access the API

API: http://localhost:8000
Interactive Docs: http://localhost:8000/docs
Alternative Docs: http://localhost:8000/redoc


📡 API Endpoints

Authentication

Method	Endpoint	    Description	                Access
POST	  /register	    Register a new user	        Public
POST	  /login	      Login and get user info	    Public

Transactions

Method	       Endpoint	           Description	              Access
POST	       /transactions	       Create a transaction	      Authenticated
GET	         /transactions	       List all transactions	    Authenticated
GET	         /transactions/{id}	   Get specific transaction	  Authenticated
PUT	        /transactions/{id}	   Update transaction	        Admin/Analyst
DELETE	    /transactions/{id}	   Delete transaction	        Admin only

Analytics

Method	              Endpoint	                          Description	             Access
GET	             /analytics/summary	                      Get financial summary	   Authenticated
GET	        /analytics/category-breakdown/{type}	        Category analysis	       Authenticated
GET	               /analytics/monthly	                      Monthly trends	       Authenticated

System

Method	        Endpoint	        Description
GET	              /	            Welcome message
GET	            /health	          Health check


## Sample Usage

### 1. Register a User

curl -X POST "http://localhost:8000/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe",
    "email": "john@example.com",
    "password": "john123",
    "role": "analyst"
  }'

### 2. Login

curl -X POST "http://localhost:8000/login?username=john_doe&password=john123"

### 3. Create an Income Transaction

curl -X POST "http://localhost:8000/transactions?user_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 5000,
    "type": "income",
    "category": "Salary",
    "description": "Monthly salary"
  }'

### 4. Create an Expense Transaction

curl -X POST "http://localhost:8000/transactions?user_id=1" \
  -H "Content-Type: application/json" \
  -d '{
    "amount": 200,
    "type": "expense",
    "category": "Groceries",
    "description": "Weekly shopping"
  }'

### 5. Get All Transactions

curl -X GET "http://localhost:8000/transactions?user_id=1"

### 6. Get Financial Summary

curl -X GET "http://localhost:8000/analytics/summary?user_id=1"

### 7. Get Category Breakdown

curl -X GET "http://localhost:8000/analytics/category-breakdown/expense?user_id=1"

