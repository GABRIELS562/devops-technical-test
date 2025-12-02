import pytest
import os
from typing import Generator
from app import app, db
from sqlalchemy import text


@pytest.fixture
def client() -> Generator:
    """
    Test client fixture with database setup and teardown.

    Fix: reviewed test setup - original relied on alembic.ini which is gitignored.
    Simplified to use SQLAlchemy directly and seed minimal test data for API tests.
    """
    app.config['TESTING'] = True

    client = app.test_client()

    with app.app_context():
        # Create tables directly - simpler than alembic for test env
        db.create_all()

        # Create candidates table if not exists (matches main app schema)
        db.session.execute(text('''
            CREATE TABLE IF NOT EXISTS candidates (
                id SERIAL PRIMARY KEY,
                full_names TEXT,
                surname TEXT,
                party TEXT,
                age TEXT,
                gender TEXT,
                orderno TEXT,
                list_type TEXT,
                candidate_type TEXT
            )
        '''))

        # Seed test data for API endpoint tests
        # Ward 1 needs at least one candidate for test_api.py to pass
        db.session.execute(text('''
            INSERT INTO candidates (full_names, surname, party, age, gender, orderno, list_type, candidate_type)
            VALUES
                ('John', 'Doe', 'Test Party A', '45', 'Male', '1', 'Ward 1', 'national_regional'),
                ('Jane', 'Smith', 'Test Party B', '38', 'Female', '1', 'Ward 1', 'national_regional'),
                ('Bob', 'Johnson', 'Test Party A', '52', 'Male', '2', 'Ward 1', 'national_regional')
        '''))
        db.session.commit()

    yield client

    with app.app_context():
        # Clean up after tests
        db.session.execute(text('DROP TABLE IF EXISTS candidates'))
        db.session.commit()
        db.drop_all() 
