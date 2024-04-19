import pdb
import logging
import financials
import signal
from decimal import Decimal
import pytz
from datetime import datetime
import schedule
import time
from pandas_market_calendars import get_calendar
from tastytrade import Account, order
from tastytrade.order import NewOrder
import file_ops

tasty_session = None # for use in other methods in this module

# Define the timezone for New York
ny_timezone = pytz.timezone('America/New_York')

# Get the NYSE trading calendar
nyse_calendar = get_calendar('NYSE')

def _is_trading_day():
    trading_day = False
    # Get the current time in New York timezone
    current_time = datetime.now(ny_timezone)
    
    # Check if it's a trading day on the NYSE  
    if nyse_calendar.valid_days(start_date=current_time.date(), end_date=current_time.date()).size > 0:
        trading_day = True
    
    return trading_day

# Define the functions to be executed at specific times
def task_09_30_ny():
    logging.info('It\'s 9.30 in NY, check if there something to do in the markets today....')
    
    if _is_trading_day():
        # get net liquidity value
        logging.info('Markets open, dingdingding....')
    else:
        logging.info('Markets closed today.')

def task_16_00_ny():
    logging.info('It\'s 4pm in NY, checking if the markets were open today.')

    account = Account.get_accounts(tasty_session)[0]
    if _is_trading_day():
        try:
            net_liq_value = account.get_balances(tasty_session).net_liquidating_value
            positions = account.get_positions(tasty_session, instrument_type=order.InstrumentType.EQUITY)
            position_symbols = [position.symbol for position in positions]

            net_liq_value = account.get_balances(tasty_session).net_liquidating_value

            with open(file_ops.symbols_open_positions_path, 'w') as file:
                # Write data
                for symbol in position_symbols:
                    file.write(f'{symbol}\n')

            with open(file_ops.account_balances_path, 'w') as file:
                file.write(f'NetLiquidatingValue,{net_liq_value}\n')    

            financials.process_symbols('open_positions')
        except Exception as e:
            raise
        logging.info('Do something after markets close.')
    else:
        logging.info('Markets closed today.')


# Schedule the tasks at specific times in New York time on weekdays that are also trading days on NYSE
def schedule_tasks(trading_session):
    global tasty_session
    tasty_session = trading_session

    # Schedule task at 9:30 AM New York time
    schedule.every().day.at('09:30', ny_timezone).do(task_09_30_ny)

    # Schedule task at 10:00 PM New York time
    schedule.every().day.at('16:00', ny_timezone).do(task_16_00_ny)

    logging.info('Tasks are scheduled. Waiting for the action......')

    # Keep the program running to execute scheduled tasks
    while True:
        schedule.run_pending()
        time.sleep(1)

# Define the signal handler to stop the program gracefully
def signal_handler(sig, frame):
    print("Stopping program...")
    logging.info('Closing Tasty Trade connection due to user interruption.')
    tasty_session.destroy()
    # You can perform any cleanup tasks here before exiting
    exit(0)

# Register the signal handler for SIGINT (Ctrl-C)
signal.signal(signal.SIGINT, signal_handler)

