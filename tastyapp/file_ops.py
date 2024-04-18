import os

SYMBOLS_CANDIDATES = 'symbols_candidates.csv'
SYMBOLS_CANDIDATES_OUT = 'symbols_candidates_out.csv'
SYMBOLS_OPEN_POSITIONS = 'symbols_open_positions.csv'
SYMBOLS_OPEN_POSITIONS_OUT = 'symbols_open_positions_out.csv'

current_dir = os.path.dirname(os.path.abspath(__file__))
symbols_candidates_path = os.path.join(current_dir, '..', 'data', SYMBOLS_CANDIDATES)
symbols_sys_output_path = os.path.join(current_dir, '..', 'data', SYMBOLS_CANDIDATES_OUT)
symbols_open_positions_path = os.path.join(current_dir, '..', 'data', SYMBOLS_OPEN_POSITIONS)
symbols_open_positions_out_path = os.path.join(current_dir, '..', 'data', SYMBOLS_OPEN_POSITIONS_OUT)

