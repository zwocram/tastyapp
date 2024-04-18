import argparse
import os
import yfinance as yf
import pandas_ta as ta
import pandas as pd

import file_ops
import pdb




def get_stock_data(symbol):
    try:
        # Retrieve historical stock data
        stock = yf.Ticker(symbol)
        hist_data = stock.history(period="250d")  # Get today's data

        # Calculate technical indicators
        hist_data.ta.atr(length=14, append=True)  # ATR(14)
        hist_data.ta.sma(length=200, append=True)  # SMA(200)
        hist_data.ta.rsi(length=3, append=True)  # RSI(3)

        # Get the lowest price in the last three business days
        last_3_days_lowest_price = hist_data['Low'].tail(3).min()

        # Calculate ATR(14) / Close Price
        atr_close_ratio = round(hist_data['ATRr_14'].iloc[-1] / hist_data['Close'].iloc[-1], 4)

        return {
            'symbol': symbol,
            'last_close_price': round(hist_data['Close'].iloc[-1], 2),
            'sma_200': round(hist_data['SMA_200'].iloc[-1], 2),
            'atr_14': round(hist_data['ATRr_14'].iloc[-1], 4),
            'rsi_3': round(hist_data['RSI_3'].iloc[-1], 2),
            '3DLow': round(last_3_days_lowest_price, 2),
            'atr_close_ratio': atr_close_ratio
        }
    except Exception as e:
        print(f"Failed to get data for ticker '{symbol}' reason: {e}")
        return None

def process_symbols(symbol_type):

    file_path = None
    if symbol_type == 'candidates':
        file_path = file_ops.symbols_candidates_path
    elif symbol_type == 'open_positions':
        file_path = file_ops.symbols_open_positions_path
        file_path_out = file_ops.symbols_open_positions_out_path

    with open(file_path, 'r') as symbols_file:
        symbols = symbols_file.read().splitlines()

    stock_data = [get_stock_data(symbol) for symbol in symbols if get_stock_data(symbol)]
    symbols_df = pd.DataFrame(stock_data)
    symbols_df_sorted = symbols_df.sort_values(by='atr_close_ratio', ascending=False)
    symbols_df_sorted.insert(1, 'status', 'TBO')

    print(symbols_df)

    symbols_df_sorted.to_csv(file_ops.symbols_sys_output_path, index=False, sep='\t')
    if symbol_type == 'candidates':
        symbols_df_sorted.to_csv(file_ops.symbols_sys_output_path, index=False, sep='\t')
    elif symbol_type == 'open_positions':
        symbols_df_sorted.to_csv(file_ops.symbols_open_positions_out_path, index=False, sep='\t')

    symbols_file.close()
    

if __name__ == "__main__":  
    # Main parser
    parser = argparse.ArgumentParser(description="Get and modify financial data for stock symbols.")

    # Add subparsers for each command
    subparsers = parser.add_subparsers(dest="command", help="Subcommands")

    # Subparser for the EOD command
    parser_eod_date = subparsers.add_parser("market_data", help="Retrieve EOD data for symbols.")
    parser_eod_date.set_defaults(func=process_symbols('candidates'))

    # Subparser for Command 2
    #parser_financials = subparsers.add_parser("financials", help="Do things with market data from yahoo.")
    #parser_financials.set_defaults(func=financials)

    # Parse the command-line arguments
    args = parser.parse_args()

    # Execute the appropriate function based on the subcommand
    if hasattr(args, 'func'):
        args.func()
    else:
        print("No command specified. Use -h or --help for usage information.")