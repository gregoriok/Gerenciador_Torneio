import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
import psycopg2
from app.main import app
from app.database import Base, get_db

DB_USER = "admin"
DB_PASSWORD = "admin"
DB_HOST = "localhost"
DB_PORT = "5432"
TEST_DB_NAME = "test_futebol_db"

ADMIN_DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/postgres"
# URL para o banco de dados de teste que será criado e usado
TEST_DB_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{TEST_DB_NAME}"

def create_test_database_if_not_exists():
    """Conecta-se ao BD admin 'postgres' e cria o banco de dados de teste se ele não existir."""
    conn = None
    try:
        # Conecta-se ao banco de dados 'postgres' que sempre existe
        conn = psycopg2.connect(ADMIN_DB_URL)
        conn.autocommit = True  # CREATE DATABASE não pode ser executado em uma transação
        cursor = conn.cursor()

        # Verifica se o banco de dados de teste já existe
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{TEST_DB_NAME}'")
        exists = cursor.fetchone()

        if not exists:
            print(f"\nBanco de dados '{TEST_DB_NAME}' não encontrado. Criando...")
            cursor.execute(f"CREATE DATABASE {TEST_DB_NAME}")
            print(f"Banco de dados '{TEST_DB_NAME}' criado com sucesso.")
        else:
            print(f"\nBanco de dados '{TEST_DB_NAME}' já existe.")

        cursor.close()
    except Exception as e:
        print(f"Ocorreu um erro ao tentar criar o banco de dados: {e}")
        # Se não conseguir conectar/criar, o melhor é falhar os testes
        pytest.fail(f"Não foi possível configurar o banco de dados de teste: {e}")
    finally:
        if conn:
            conn.close()

engine = create_engine(TEST_DB_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    create_test_database_if_not_exists()
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """
    Fornece uma sessão de banco de dados para um teste, garantindo que
    todas as alterações sejam desfeitas (rollback) após o teste.
    Pois caso nao faça isso os testes vazam de um para outro.
    """
    connection = engine.connect()
    transaction = connection.begin()
    db = TestingSessionLocal(bind=connection)
    try:
        yield db
    finally:
        db.close()
        transaction.rollback()
        connection.close()

@pytest.fixture()
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()