import subprocess
import sys
import time
import os

def run_main_infinite():
    i = 0
    e = 0
    while True:
        try:
            # Run main.py
            os.system("cls")
            
            print(f'''
                  ###############################
                  ########## Success: {i}   #######
                  ########## Error  : {e}   #######
                  ###############################
                  ''')
            subprocess.run(['python', 'droplink.py'], check=True)
            i += 1
            
        except subprocess.CalledProcessError as err:
            e += 1
            print(f"An error occurred: {err}")
            break  # Exit the loop if an error occurs
        
        except Exception as ex:
            e += 1
            print(f"An unexpected error occurred: {ex}")
            break  # Exit the loop if an unexpected error occurs
        
        time.sleep(1)

if __name__ == "__main__":
    run_main_infinite()
