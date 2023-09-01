# utilities for DaCondor54 Bot

import re

class InvalidTimeException(Exception):
    pass

def time_parser(time : str) -> (int ,int):
    match = re.search('^(?P<min>[0-5]?[0-9]m){0,1}(?P<sec>[0-5]?[0-9]s){0,1}$', time)
    if match:
        minutes = process_time_value(match.group('min'))        
        seconds = process_time_value(match.group('sec'))                
        print(f'value : {minutes} {seconds}')
        return (int(minutes), int(seconds)) 
    raise InvalidTimeException('**Invalid Time for Timer**')

def process_time_value(time_value : str) -> str :
    return time_value[:-1] if time_value else '0'    