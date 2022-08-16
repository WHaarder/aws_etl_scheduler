from sqlalchemy import create_engine
from urllib.parse import quote_plus


def db_connect():
    pw = quote_plus("28H0!p3UNWkpQ#GBL1%Wh%uK")
    print("ssss")
    eng = create_engine(
        f"postgresql+psycopg2://postgres:{pw}@database-1.cdk0hw21r49l.eu-central-1.rds.amazonaws.com"
    )
    conn = eng.connect()
    test = eng.execute(
        """SELECT *
            FROM pg_catalog.pg_tables;
            """
    ).fetchall()
    print(test)
    conn.close()
