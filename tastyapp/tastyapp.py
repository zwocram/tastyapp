
import logging
import connect
import pdb
import json
import schedules as sch

import argparse

def main(environment):
    session = connect.connect_tt(environment)
    return session

if __name__ == "__main__":  
    # Parse command-line arguments
    parser = argparse.ArgumentParser(description="Choose Tasty environment")
    parser.add_argument('--environment', default='sandbox', choices=['sandbox', 'production'],
            help="Specify environment (default: test)")
    args = parser.parse_args()

    try:
        session = main(args.environment)
        sch.schedule_tasks(session)
    except Exception as e:
        logging.error(f"Error occurred while creating sandbox session: {e}")
        raise
    finally:
        if session.validate():
            logging.info("Closing TastyTrade connection.")
            session.destroy()
