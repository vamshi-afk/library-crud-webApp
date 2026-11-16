# Library of Arch — Library Management System

A full-stack Library Management System built with **FastAPI**, **SQLAlchemy 2.0**, and **PostgreSQL**. Designed with strict relational integrity, N+1 query prevention, PII data minimization via Pydantic schemas, and automated overdue fine calculation.

## Features

- **Book Catalog Management:** Add books with copy tracking (`total_copies` vs. `available_copies`), case-insensitive search (`ILIKE`) across titles and authors, and protected deletion.
- **Member Registry:** Register library members with unique email enforcement and active-loan deletion guards.
- **Checkout & Return Lifecycle:**
  - Enforces copy availability and prevents duplicate active checkouts by the same member.
  - Automatically assigns a 7-day UTC due date on checkout and calculates daily overdue penalties (`₹10/day`) upon return.
- **Relational Integrity & Performance:**
  - Uses SQLAlchemy `relationship()` and `joinedload()` to resolve nested book and member details in a single `LEFT OUTER JOIN` query (eliminating N+1 query bottlenecks).
  - Catches PostgreSQL `IntegrityError` constraints with clean session rollbacks (`db.rollback()`) to preserve historical borrow records.
- **Data Minimization:** Exposes stripped-down response schemas (`MemberPublic`) on loan endpoints so sensitive member PII (such as email addresses) is never leaked over the network.

## Tech Stack

- **Backend:** Python 3.14, FastAPI, Uvicorn
- **ORM & Database:** SQLAlchemy 2.0, PostgreSQL (`psycopg` v3)
- **Validation & Serialization:** Pydantic v2
- **Frontend:** Jinja2 Templates, Vanilla JavaScript (`fetch`), Bootstrap 5
- **Tooling:** `uv` (package & lockfile management), Ruff (linting & import sorting)

## Project Structure

```text
.
├── app/
│   ├── __init__.py
│   ├── database.py        # SQLAlchemy engine, session lifecycle, and DbSession dependency
│   ├── main.py            # FastAPI app initialization, static mounts, and router registration
│   ├── models.py          # Declarative ORM models (Book, Member, BorrowRecord)
│   ├── schemas.py         # Pydantic request/response schemas and data-minimization models
│   └── routers/
│       ├── books.py       # Catalog CRUD, ILIKE search, and foreign-key deletion guards
│       ├── members.py     # Member registration, uniqueness checks, and deletion guards
│       └── borrow.py      # Checkout/return transactions, joinedload queries, and fine math
├── static/
│   └── script.js          # Frontend API integration
├── templates/
│   └── index.html         # Single-page Bootstrap dashboard
├── pyproject.toml         # Project metadata and direct dependencies
└── uv.lock                # Cross-platform deterministic dependency lockfile
```

## Getting Started

### Prerequisites

- Python `>=3.14`
- PostgreSQL running locally
- [`uv`](https://docs.astral.sh/uv/) installed

### Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/vamshi-afk/lib-app.git
   cd lib-app
   ```

2. **Install dependencies with `uv`:**
   ```bash
   uv sync
   ```

3. **Configure environment variables:**
   Create a `.env` file in the project root with your PostgreSQL connection string:
   ```env
   DATABASE_URL=postgresql+psycopg://<username>:<password>@localhost:5432/<database_name>
   ```

4. **Run the development server:**
   ```bash
   uv run fastapi dev app/main.py
   ```

5. **Access the application:**
   - **Web UI:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
   - **Interactive Swagger API Docs:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

## API Overview

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/books/?search=` | List all books or filter by title/author (`ILIKE`) |
| `POST` | `/books/` | Add a new book to the catalog |
| `DELETE` | `/books/{book_id}` | Delete a book (blocked if checked out or in borrow history) |
| `GET` | `/members/` | List all registered members |
| `POST` | `/members/` | Register a new member (enforces unique email) |
| `DELETE` | `/members/{member_id}` | Remove a member (blocked if active loans or history exist) |
| `GET` | `/borrow/` | List all borrow records with nested book & public member info |
| `POST` | `/borrow/` | Issue a book copy and set a 7-day due date |
| `PUT` | `/borrow/return/{record_id}` | Return a book, restore inventory, and compute overdue fines |