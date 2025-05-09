import os
import sys
import shutil 

R = "\033[91;1m"  # Red
G = "\033[92;1m"  # Green
B = "\033[94;1m"  # Blue
Y = "\033[93;1m"  # Yellow
C = "\033[96;1m"  # Cyan
M = "\033[95;1m"  # Magenta
W = "\033[97;1m"  # White
D = "\033[90;1m"  # Grey
S = "\033[0m"     # Reset

sign = "\033[92;1m" + "[" + "\033[94;1m" + "*" + "\033[92;1m" + "]" + "\033[94;1m"
Enter = "\033[94;1m" + "[" + "\033[92;1m" + "+" + "\033[94;1m" + "]" + "\033[92;1m"
ERROR = "\033[93;1m" + "×" + " " + "\033[91;1m" + "ERROR ⚠\n" + "\033[93;1m" + "╰─> " + "\033[93;1m"
INFO = "\033[93;1m" + "[" + "\033[92;1m" + "INFO" + "\033[93;1m" + "]" + "\033[94;1m"
please = "\033[93;1m" + "[" + "\033[91;1m" + "!" + "\033[93;1m" + "]" + "\033[91;1m"
Running = "\033[94;1m" + '[Running]' + "\033[95;1m"

def uninstall():
    try:
        while True:
            print(f' {G}[1] {B}Uninstall Manager PC{W}\n',f'{G}[2] {B}Exit{W}\n')
            
            uninstall_choice = input(f'{Enter} Enter your choice: {Y}')

            if uninstall_choice == '1':
                items_to_remove = [
                    'LICENSE'
                    'README.md'
                    'setup.bat',
                    'update.bat' 
                    'versoin.txt'
                    'ixdbg.py'
                ]

                for item in items_to_remove:
                    if os.path.exists(item):
                        if os.path.isfile(item):
                            os.remove(item)
                            print(f'{INFO} File removed: {item}')
                        elif os.path.isdir(item):
                            shutil.rmtree(item)
                            print(f'{INFO} Folder removed: {item}')
                    else:
                        print(f'{please} Not found: {item}{W}')
                
                with open("cleanup.bat", "w") as batch_file:
                    batch_file.write(f"@echo off\n")
                    batch_file.write(f"timeout /t 2 >nul\n")
                    batch_file.write(f"del \"{__file__}\"\n")
                    batch_file.write(f"del cleanup.bat\n")
                
                print(f"{Running} Uninstallation complete Closing...{W}")
                
                os.system("start cleanup.bat")
                sys.exit()

            elif uninstall_choice == '2':
                print(f"{Running} Exiting...{W}")
                sys.exit()

            else:
                print(f"{ERROR} choice Please try again !{W}")
    except KeyboardInterrupt:
        print(f"\n{sign} Process interrupted by user.{W}")
        sys.exit()

if __name__ == '__main__':
    uninstall()