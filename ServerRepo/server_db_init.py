from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class Connector:
    def __init__(self, db):
        self.engine = create_engine('sqlite:///' + db)

    def __enter__(self):
        self.session = sessionmaker(bind=self.engine)()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect_db()

    def disconnect_db(self):
        self.session.commit()
        self.session.close()


