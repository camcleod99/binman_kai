from datetime import datetime, timedelta
from setup import init_app
from database import *
from server import *
from logger import init_log

# GLOBALS
DEFAULT_URL = "https://www.eastdunbarton.gov.uk/services/a-z-of-services/bins-waste-and-recycling/bins-and-recycling/collections/?uprn=132015695&m="
DEFAULT_DATE = "1970-01-01 00:00:00.000000"

log = init_log("main")

if __name__ == "__main__":
    soup = Soup()
    app = init_app()

    # Initialise Database
    if not os.path.exists(db_path):
        data_site = soup.get_data(DEFAULT_URL)
        update_timestamp = str(datetime.now())
        log.info(f"Database not found at {db_path}. Initializing...")
        data_init(DEFAULT_URL, data_site, update_timestamp)
    else:
        log.info(f"Database found at {db_path}.")

    # Read Database
    with app.app_context():
        data_bins = data_load_table(app, Bins)
        data_system = data_load_table(app, System)
        values = {row.key: row.value for row in data_system}
        data_system_url = values.get("target_url")
        data_system_last_update = values.get("last_update")
        log.info(f"{data_system_url},{data_system_last_update}")
        if data_system_url is None:
            log.warning("System table is missing taret url, setting to default")
            url_update(app, DEFAULT_URL)
        if data_system_last_update is None:
            log.warning("System table is missing last update, setting to default")
            date_update(app, DEFAULT_DATE)
        log.info(f"{data_system_url},{data_system_last_update}")

    # Update if bins last update was longer than than 24 hours
    if data_system_last_update is None:
        log.info("System is initalised, Updating...")
        data_site = soup.get_data(DEFAULT_URL)
        update_timestamp = str(datetime.now())
        data_update(app, data_site, update_timestamp)
        url_update(app, DEFAULT_URL)
    elif datetime.now() - datetime.fromisoformat(data_system_last_update) > timedelta(days=1):
        log.info("Last Update was more than a day ago. Updating...")
        data_site = soup.get_data(data_system_url)
        update_timestamp = str(datetime.now())
        data_update(app, data_site, update_timestamp)
    else:
        log.info("Last Update was less than a day ago. Skipping update.")

    log.critical("MCDONALDS!")
    app.run(host="0.0.0.0", port=9595, debug=True, use_reloader=False)
