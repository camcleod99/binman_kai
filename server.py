from datetime import datetime, timedelta
from flask import render_template
from sqlalchemy.exc import SQLAlchemyError
from logger import init_log
from setup import app, db
from database import data_load_table, data_update, System, Bins
from soup import Soup

DEFAULT_URL = "https://www.eastdunbarton.gov.uk/services/a-z-of-services/bins-waste-and-recycling/bins-and-recycling/collections/?uprn=132015695&m="
log = init_log("server")

def update_setup():
    data_system_update = data_load_table(app, System)
    data_values_update = {row.key: row.value for row in data_system_update}
    url = data_values_update.get("target_url")
    last_update = data_values_update.get("last_update")
    return url, last_update

def update_data(url, last_update):
    bin_data = Soup().get_data(url)
    log.info("Successfully rendered update with message")
    log.info("Update Successful.")
    data_update(bin_data, last_update)

def update_warn_log():
    log.info("Successfully rendered update with message")
    log.warning("Last Update was more than a day ago. Skipping update.")

def get_bins():
    return db.session.execute(db.select(Bins).order_by(db.cast(Bins.collection_days, db.Integer))).scalars().all()

# FLASK - ROUTES
@app.route("/")
def index():
    try:
        data_load_table(app, Bins)
        items = db.session.execute(
            db.select(Bins).order_by(db.cast(Bins.collection_days, db.Integer))
        ).scalars().all()
        if items:
            log.info("Successfully rendered index.html")
            return render_template("index.html", items=items)
        else:
            return render_template("index.html", message_type="error", message="No rows in Bins.")
    except SQLAlchemyError as e:
        error_message = f"SQLAlchemyError in index(): {e}"
        log.critical(error_message)
        return render_template("index.html", message_type="danger", message=error_message)

@app.route("/update")
def update():
    url, last_update = update_setup()
    if datetime.now() - datetime.fromisoformat(last_update) > timedelta(days=1):
        update_data(url, last_update)
        items = get_bins()
        return render_template("index.html", items=items, update_type="success", message="Update Successful.")
    else:
        items = get_bins()
        update_warn_log()
        return render_template("index.html", items=items, update_type="warning", message="Last Update was less than a day ago. Skipping update." )

@app.route("/update/api", methods=["POST"])
def update_api():
    url, last_update = update_setup()
    if datetime.now() - datetime.fromisoformat(last_update) > timedelta(days=1):
        update_data(url, last_update)
        return {"status": "success", "message": "Update Successful."}
    else:
        update_warn_log()
        return {"status": "warning", "message": "Last Update was less than a day ago. Skipping update."}
