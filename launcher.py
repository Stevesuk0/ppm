#!/usr/bin/python3

from colorama import init, Fore, Style, Back
import sys
import os
import time

init(autoreset=False) # init colorama
sys.setrecursionlimit(1500) 

# Define different message types with colored formatting
info_character = '##'
success = f"{Fore.GREEN}{info_character}{Fore.RESET}"
info = f"{Fore.BLUE}{info_character}{Fore.RESET}"
warn = f"{Fore.YELLOW}{info_character}{Fore.RESET}"
error = f"{Fore.RED}{info_character}{Fore.RESET}"

version = "0.1.1"
launcher_dir = '/opt/ppm'
cache_dir = '/var/cache/ppm'
config_dir = '/etc/ppm'
locale_dir = '/opt/ppm/localization'

os.makedirs(cache_dir, exist_ok=True)
os.makedirs(config_dir, exist_ok=True)
os.makedirs(launcher_dir, exist_ok=True)
os.makedirs(locale_dir, exist_ok=True)

sys.path.append(launcher_dir) # Add custom path for ppm modules
import modules
import modules.auth
import modules.managing
import modules.config
import modules.lock

modules.lock.cache_dir = cache_dir
modules.managing.cache_dir = cache_dir
modules.managing.config_dir = config_dir
modules.config.cache_dir = cache_dir
modules.config.config_dir = config_dir

print(f'ppm {version}')

help_text = """
Usage: ppm [options] command

ppm is a command-line package manager currently under testing.
If you encounter any issues while using ppm, please report them at [https://github.com/Stevesuk0/ppm/issues].

This software is free and follows the GNU General Public License v2.

Common commands:
init         Initialize configuration files and software sources
reset        Force remove ppm process lock
refresh      Synchronize the dpkg database
update       Update the package list
search       Search a packages by keyword
clean        Clean ppm cache files"""

def main():
    if len(sys.argv) < 2:
        print(f"{error} Not enough arguments provided.")
        print(help_text)
        exit()
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    if command == 'init':
        if modules.config.initRepoConfig():
            print(f'{success} The configuration file has been initialized.')
    
    elif command == 'search':
        start = time.time()
        repolist = modules.config.getRepofromCache() 
        for repo in repolist:
            for package_name in args:
                packinfo = modules.managing.searchPackage(package_name, repo)
                if packinfo:
                    print(f"{packinfo['Package']}, {packinfo['Version']}")
        
        # with os.popen(f"find.go {args[-1]}") as f: print(f.read(), end='')

        print(round((time.time() - start) * 1000, 1), 'ms')



    elif command == 'clean':
        cleaning = modules.config.cleanCacheFolder()
        if cleaning[0]: # bool
            if cleaning[1] == 0:
                print(f"{info} Nothing to clean.") 
            else:
                print(f"{success} Successfully clean {cleaning[1]} cache files.")
        else:
            print(f"{error} Failed to clean cache files.")

    elif command == 'refresh':
        print(f"{info} Refreshing...")
        installed = modules.managing.dpkg_refreshInstalled()
        print(f"{info} The current system has {installed} dpkg packages installed.")

    elif command == 'help':
        print(help_text)

    elif command == 'update':
        repos = modules.config.getRepofromConfiguation()
        print(f"{info} Found {len(repos)} repositories from configuration...")
        for repo in repos:
            print(f"{info} Updating package list: {repo['name']} ({repo['type']})...", end='')
            sys.stdout.flush()
            if modules.managing.updateMetadata(repo)[0]:
                print(f"\r{success} Updated package list: {repo['name']} ({repo['type']})...")
            else:
                print(f"\r{warn} Unable to parse repo \"{repo['name']} ({repo['type']})\", ignoring this item.")

    elif command == 'reset':
        if modules.lock.disable():
            print(f"{success} Successfully removed the lock file.")
        else:
            print(f"{error} Failed to remove the lock file.")
        
    else:
        print(f"{error} Provided command not found.")

if __name__ == "__main__":
    if modules.auth.checkIsRoot() is False:
        print(f"{warn} Running ppm as normal user.")
        modules.auth.run_as_root(" ".join(sys.argv[1:]))
        exit() 
    
    main()
else:
    print(f"{error} Directly importing ppm launcher is not recommend for managing system packages, you should be importing the modules of ppm, not the launcher.")
    print(f"{info} See more infomation at https://wiki.ppm.mom/importing-launcher")
