from tastytrade import CertificationSession, ProductionSession

import secretdata
import logging


def connect_tt(environment):

    # Set up logging configuration
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    session = None

    try:
        secrets = secretdata.read_secrets()

        if environment == 'production':

            username_prd = secrets.get("username_prd")
            password_prd = secrets.get("password_prd")
            account_number_prd = secrets.get("account_number_prd")

            if None in (username_prd, password_prd, account_number_prd):
                raise ValueError("One or more secrets are missing")

            try:
                session = ProductionSession(username_prd, password_prd)
            except Exception as e:
                logging.error(f"Error occurred while creating production session: {e}", exc_info=True)

        else:
            username_sandbox = secrets.get("username_sandbox")
            password_sandbox = secrets.get("password_sandbox")
            account_number_sandbox = secrets.get("account_number_sandbox")

            if None in (username_sandbox, password_sandbox, account_number_sandbox):
                raise ValueError("One or more secrets are missing")

            try:
                session = CertificationSession(username_sandbox, password_sandbox)
            except Exception as e:
                logging.error(f"Error occurred while creating sandbox session: {e}", exc_info=True)

    except Exception as e:
        # Handle any exceptions that occur during secret retrieval
        logging.error(f"Error occurred while retrieving secrets: {e}. Does the file data/secrets.json exist?", exc_info=True)

    if session is None:
        logging.error("Could not create a valid Tasty session.")
    else:
        logging.info("Checking validaty of the Tasty Session...")
        logging.info(session.validate())
        return session
