import psutil
import sys
import os.path as path

APPLICATION_ID = "Bioshock2.exe"
SHOCKMPGAME_ADAM_REQUIREMENTS = 41
DLC_ADAM_REQUIREMENTS = 10
DLC_MIN_RANK = 50

# Class: DIRECTORIES
# Stores the directories of the user's files.
# Also has default mRankAdamRequirements values for easy default restoration.
class DIRECTORIES:

    def __init__ (self, DLC1, DLC2, SHOCKMPGAME, USERMP, CUSTOM_RANK):
        self.DLC1 = DLC1
        self.DLC2 = DLC2
        self.SHOCKMPGAME = SHOCKMPGAME
        self.USERMP = USERMP
        self.CUSTOM_RANK = CUSTOM_RANK
    
    SHOCKMPGAME_DEFAULT_REQUIREMENTS = [
        0, 0, 500, 1000, 2000, 3000, 4000, 5000, 6000, 7000, 9000, 10500, 12000, 13500, 
        15000, 16500, 18000, 19500, 21000, 22500, 25500, 28000, 30500, 33000, 35500, 
        38000, 40500, 43000, 45500, 48000, 53000, 57000, 61000, 65000, 69000, 73000, 
        77000, 81000, 85000, 89000, 97000
    ]

    DLC_DEFAULT_REQUIREMENTS = [
        103000, 109000, 115000, 121000, 127000, 133000, 139000, 145000, 151000, 163000
    ]

global DIRECTORY

# Function: process_active()
# Checks if the Bioshock 2 process is active and located in the Multiplayer Directory, not the Singleplayer Directory.
# Returns the directory of the process for locating purposes.
# Return : bool : True if the directory of the Bioshock 2 process is under Multiplayer. False if Singleplayer or not active.
# Return : directory : The directory of the Bioshock 2 process if it is active and located in the Multiplayer Directory, otherwise None.
#
def process_active():
    directory = None
    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        if proc.info['name'] == APPLICATION_ID:
            directory = proc.info['exe']
            break

    return directory is not None and "\\MP\\" in directory, directory

# Function: process_terminate()
# Closes Bioshock 2 Multiplayer.
def process_terminate():
    for proc in psutil.process_iter(['pid', 'name', 'exe']):
        if proc.info['name'] == APPLICATION_ID:
            proc.terminate()

# Function: options()
# The main function of the program, which prompts the user to select a specific functionality.
# Choice 1 implements the Rank Fix feature, ensuring the user ranks up to level 50 in a single match.
# Choice 2 allows the user to set custom ranks up to level 100 (capped). Note: This choice also calls the Rank Fix function to scale mRankAdamRequirements properly.
# Choice 3 restores the user's files back to their default state.
# Choice 4 terminates the program.
def options():
    global DIRECTORY
    DIRECTORY = DIRECTORIES("", "", "", "", 0)

    print("\nWhat would you like to do: \n")
    print("1. Rank 50 Fix")
    print("2. Give Custom Rank")
    print("3. Restore Default Rank Adam Required")
    print("4. Quit")

    while True:
        try:
            user_choice = int(input("Option: "))
            if user_choice < 1 or user_choice > 4:
                raise ValueError
            break 
        except ValueError:
            print("Error Invalid Input: Please enter a NUMERICAL value between [1 - 4]\n")

    if user_choice == 4:
        quit()

    rank_directories()
    generalize_adam_requirements()
    
    if user_choice == 1:
        fix_rank()
        print("\nRank 50 Fix has been applied to ShockMPGAME.ini, dlc1unlocks.ini and dlc2unlocks.ini.")
        print("Please Play 1 Private Match or 1 Public Match to Reach Rank 50.")
    elif user_choice == 2:
        fix_rank()
        custom_rank()
        print(f"\nRank {DIRECTORY.CUSTOM_RANK} has been applied to dlc2unlocks.ini.")
        print(f"Please Play 1 Private Match or 1 Public Match to Reach Rank {DIRECTORY.CUSTOM_RANK}.")
    elif user_choice == 3:
        default_rank()
        print("\nDefault mRankAdamRequirements has been restored for ShockMPGAME.ini, dlc1unlocks.ini and dlc2unlocks.ini.")


    if process_active():
        print("\nBioshock 2 Multiplayer will be Closed. Please Re-Open for Changes to be Applied.")
        process_terminate()

    input("Enter to Exit.....")
    quit()

# Function: fix_rank()
# Modifies the level files to ensure that players reach level 50 by adjusting the mRankAdamRequirements.
# This fix guarantees that achieving level 50 requires completing either 1 Private Match or 1 Public Match, regardless of the player's current level.
def fix_rank():
    rank, initial_ranks = 0, 0
    for file_path in [DIRECTORY.SHOCKMPGAME, DIRECTORY.DLC1, DIRECTORY.DLC2]:
        try:
            if file_path != DIRECTORY.SHOCKMPGAME:
                rank = 40

            with open(file_path, "r")  as f:
                file_content = f.readlines()

            for i, line in enumerate(file_content):
                if "mRankAdamRequirements" in line:
                    if file_path == DIRECTORY.SHOCKMPGAME:
                        if initial_ranks < 2:
                            rank = 0
                            initial_ranks += 1
                    file_content[i] = "mRankAdamRequirements=" + str(rank) + "\n"
                    rank = rank + 1

            with open(file_path, "w") as f:
                f.writelines(file_content)

        except FileNotFoundError:
            error_handler("Error: Problem Modifying " + file_path.split("\\")[-1] + ". Was the File Moved or Deleted? The Program will now Close.", True)


# Function: custom_rank()
# Adds additional mRankAdamRequirements to the 'dlc2unlocks.ini' configuration file.
# This function ensures that the user-defined rank falls within a specified range to prevent excessively large or small ranks.
def custom_rank():
    try:
        starting_rank = 40
        while True:
            try:
                print("\nWhat Rank Do You Want to Be: ")
                DIRECTORY.CUSTOM_RANK = int(input())
                if DIRECTORY.CUSTOM_RANK < DLC_MIN_RANK or DIRECTORY.CUSTOM_RANK > 100:
                    raise ValueError
                break 
            except ValueError:
                print("Error Invalid Rank: Please enter a NUMERICAL value between [" + str(DLC_MIN_RANK) + " - 100]\n")

        with open(DIRECTORY.DLC2, "r")  as f:
            file_content = f.readlines()
        
        file_content = update_adam_requirements(DIRECTORY.CUSTOM_RANK - starting_rank, file_content)

        with open(DIRECTORY.DLC2, "w") as f:
            f.writelines(file_content)

    except FileNotFoundError:
        error_handler("Error: Problem Modifying " + DIRECTORY.DLC2.split("\\")[-1] + ". Was the File Moved or Deleted? The Program will now Close.", True)

# Function: default_rank()
# Restores the default mRankAdamRequirements to the user's files.
def default_rank():
    for file_path in [DIRECTORY.SHOCKMPGAME, DIRECTORY.DLC1, DIRECTORY.DLC2]:
        try:
            with open(file_path, "r")  as f:
                file_content = f.readlines()
            
            rank_index = 0
            for i, line in enumerate(file_content):
                if "mRankAdamRequirements" in line:
                    if file_path == DIRECTORY.SHOCKMPGAME:
                        file_content[i] = "mRankAdamRequirements=" + str(DIRECTORY.SHOCKMPGAME_DEFAULT_REQUIREMENTS[rank_index]) + "\n"
                    else:
                        file_content[i] = "mRankAdamRequirements=" + str(DIRECTORY.DLC_DEFAULT_REQUIREMENTS[rank_index]) + "\n"
                    rank_index += 1

            with open(file_path, "w") as f:
                f.writelines(file_content)

        except FileNotFoundError:
            error_handler("Error: Problem Modifying " + DIRECTORY.DLC2.split("\\")[-1] + ". Was the File Moved or Deleted? The Program will now Close.", True)


# Function: update_adam_requirements()
# This function checks if the given Files have the correct number of mRankAdamRequirements.
# Calls add_adam_requirements() if the user needs more requirements.
# Calls remove_adam_requirements() if the user needs to remove requirements.
def update_adam_requirements(target_amount, file_content):
    requirements_count = 0
    last_index = -1
    last_adam_amount = -1
    for i, line in enumerate(file_content):
        if "mRankAdamRequirements" in line:
            requirements_count += 1
            last_index = i
            last_adam_amount = int(file_content[i].split("=")[-1].strip())

    if requirements_count < target_amount:
        add_amount = target_amount - requirements_count
        file_content = add_adam_requirements(requirements_count, add_amount, file_content, last_index, last_adam_amount)
    elif requirements_count > target_amount:
        remove_amount = requirements_count - target_amount
        file_content = remove_adam_requirements(requirements_count, remove_amount, file_content, last_index)
    
    return file_content


# Function: add_adam_requirements()
# This function adds mRankAdamRequirements to the given file contents.
# If no adam requirements exist in the file contents it appends the requirements to the end of the file.
# Param: current_amount = The current amount of mRankAdamRequirements within the file.
# Param: add_amount = The number of mRankAdamRequirements to be added to the file.
# Param: file_content = The file contents of the current file.
# Param: last_index = The last index of the mRankAdamRequirements in the file contents. Used to prevent overwriting of other file contents.
# Param: last_adam_amount = The adam amount of the last mRankAdamRequirements in the file contents. Used for adding additional requirements while increasing the adam amount.
def add_adam_requirements(current_amount, add_amount, file_content, last_index, last_adam_amount):
    if last_index != -1:
        for i in range (current_amount, current_amount + add_amount):
            last_adam_amount += 1
            file_content.insert(last_index + 1, f"mRankAdamRequirements={last_adam_amount}\n")
            last_index += 1
    else:
        last_adam_amount = 0
        for i in range(current_amount, add_amount):
            last_adam_amount += 1
            file_content.append( f"\nmRankAdamRequirements={last_adam_amount}")

    return file_content


# Function: remove_adam_requirements()
# This function removes mRankAdamRequirements from the given file contents.
# Param: current_amount = The current amount of mRankAdamRequirements within the file.
# Param: remove_amount = The number of mRankAdamRequirements to be removed from the file.
# Param: file_content = The file contents of the current file.
# Param: last_index = The last index of the mRankAdamRequirements in the file contents. Used to prevent overwriting of other file contents.
def remove_adam_requirements(current_amount, remove_amount, file_content, last_index):
    for i in range(current_amount - remove_amount, current_amount):
        del file_content[last_index]
        last_index -= 1
    return file_content

# Function: generalize_adam_requirements()
# Generalizes the mRankAdamRequirements on all three files to avoid anomalies from modified contents.
def generalize_adam_requirements():
    for file_path in [DIRECTORY.SHOCKMPGAME, DIRECTORY.DLC1, DIRECTORY.DLC2]:
        with open(file_path, "r")  as f:
                file_content = f.readlines()

        if file_path == DIRECTORY.SHOCKMPGAME:
            file_content = update_adam_requirements(SHOCKMPGAME_ADAM_REQUIREMENTS, file_content)
        else:
            file_content = update_adam_requirements(DLC_ADAM_REQUIREMENTS, file_content)
    
        with open(file_path, "w") as f:
            f.writelines(file_content)

# Function: rank_directories()
# Checks if Bioshock 2 Multiplayer is active and gets the file directories.
# Calls check_rank_files()
def rank_directories():
    while True:
        active, directory = process_active()
        if not active:
            print("\nPlease Open Bioshock 2 Multiplayer before Continuing")
            input("Enter to Retry.....")
        else:
            game_directory = directory
            break

    file_separator = "\\"
    game_directory = game_directory.split("\\")

    if game_directory[-1] == APPLICATION_ID:
        game_directory.pop()
        DIRECTORY.DLC1 = file_separator.join(game_directory) + "\\dlc1unlocks.ini"
        DIRECTORY.DLC2 = file_separator.join(game_directory) + "\\dlc2unlocks.ini"
        DIRECTORY.SHOCKMPGAME = file_separator.join(game_directory) + "\\ShockMPGame.ini"
    else:
        error_handler("\nError: Process Directory has Changed While Running. The Program will now Close.", True)

    check_rank_files()


# Function: check_rank_files()
# Checks if the file directories for the files are real and that the files are also real.
# Throws errors if files are missing from the given directory.
def check_rank_files():
    file_check = []

    if not path.isfile(DIRECTORY.DLC1):
       file_check.append("dlc1unlocks.ini")
    
    if not path.isfile(DIRECTORY.DLC2):
        file_check.append("dlc2unlocks.ini")

    if not path.isfile(DIRECTORY.SHOCKMPGAME):
        file_check.append("ShockMPGame.ini")
    
    if len(file_check) > 0:
        missing_files = ", ".join(file_check)
        file_error = "Error: The Following Files were moved or not found: " + missing_files + ". The Program will now Close."
        error_handler(file_error,True)

# Function: error_handler()
# Error handling function. Closes the program if required.
# Asks the user to enter a key in case of an error. So, that they can actually read the error.
# Param: error = The given error message to be printed.
# Param: close = True if the program is meant to close. False otherwise.
def error_handler(error,close):
        print(error)

        if close:
            input("Press Enter to Close.....")
            quit()

# Function: quit()
# Simply quit the program.
def quit():
    sys.exit()

# Function: main()
# Showcase banner and calls the main function options().
def main():
    print("*******************************************************************************")
    print(" \nBioshock 2 Multiplayer Rank Modifier by SnowTempest (ADTempest on YT/Twitch)\n")
    print("*******************************************************************************")
    options()

if __name__ == "__main__":
    main()