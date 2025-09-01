import os
from sqlalchemy.exc import SQLAlchemyError
from logger import init_log
from setup import db

os.makedirs(os.path.dirname(__file__) + "/instance", exist_ok=True)
db_path = os.path.join(os.path.dirname(__file__), "instance", "app.sqlite")

class Bins(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    collection_days = db.Column(db.String(80), nullable=False)
    collection_date = db.Column(db.String(80), nullable=False)


class System(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(80), nullable=False)
    value = db.Column(db.String(80), nullable=False)

log = init_log("database")

def data_init(app, default_url: str, bin_data, update_timestamp):
    with app.app_context():
        db.create_all()
        try:
            if not System.query.filter_by(key="target_url").first():
                db.session.add(System(key="target_url", value=default_url))
            if not System.query.filter_by(key="last_update").first():
                db.session.add(System(key="last_update", value=update_timestamp))
            db.session.commit()
            log.info(f"Database Initialized")
        except SQLAlchemyError as e:
            db.session.rollback()
            log.critical(f"data_init failed: {e}")
            raise

        try:
            for row in bin_data:
                db.session.add(Bins(name=row[0], collection_days=row[1], collection_date=row[2]))
            db.session.commit()
            log.info(f"Bin Data Initialized")
        except SQLAlchemyError as e:
            db.session.rollback()
            log.critical(f"data_init failed: {e}")
            raise

def data_load_table(app, table):
    table_name = table.__name__ if hasattr(table, "__name__") else str(table)
    try:
        with app.app_context():  # Explicitly set application context
            log.info(f"{table_name} loaded")
            return db.session.execute(db.select(table)).scalars().all()
    except SQLAlchemyError as e:
        log.critical(f"SQLAlchemyError in data_load_table(table={table_name}): {e}")
        raise


def data_update(app, bin_data, route_update_timestamp):
    try:
        with app.app_context():
            db.session.execute(db.delete(Bins))
            db.session.commit()
            for row in bin_data:
                db.session.add(Bins(name=row[0], collection_days=row[1], collection_date=row[2]))
            system_entry = System.query.filter_by(key="last_update").first()
            if system_entry:
                system_entry.value = route_update_timestamp
            log.info(f"Database Updated")
            db.session.commit()
    except SQLAlchemyError as e:
        log.critical(f"SQLAlchemyError in data_update: {e}")
        raise

def url_update(app, url):
    try:
        with app.app_context():
            system_entry = System.query.filter_by(key="target_url").first()
            if system_entry:
                # Update existing value
                system_entry.value = url
            else:
                # Insert if missing
                system_entry = System(key="target_url", value=url)
                db.session.commit()
            log.info(f"Database Updated")
            db.session.commit()
    except SQLAlchemyError as e:
        log.critical(f"SQLAlchemyError in data_update: {e}")
        raise