# src mc by blzsrc

Welcome to **.src mc by blzsrc**, a tool that allows you to interact with Minecraft accounts. This tool offers various functionalities such as generating random email and password combinations and checking the validity of Minecraft accounts.

## Features

- **Check Minecraft Accounts**: Validate Minecraft account credentials from an input file and save valid accounts to an output file.
- **Generate Email and Password**: Generate a specified number of random email and password combinations and save them to an input file.
- **Interactive Menu**: Use an intuitive menu to navigate through options and perform various tasks.
- **ASCII Art**: Enjoy aesthetically pleasing ASCII art displayed throughout the tool.
- **File Location Opening**: Automatically open the file location once a task is completed for easy access.

## Requirements

- Python 3.7 or higher
- aiohttp library (can be installed using `pip install aiohttp`)

## Usage

1. Clone the repository or download the script to your local machine.

2. Open a terminal and navigate to the directory where the script is located.

3. Run the script using the following command:

    ```shell
    python main.py
    ```

4. Follow the on-screen prompts to use the tool.

## Options

- **1. Check Minecraft Accounts**: This option reads account credentials from `unchecked-mc.txt` and checks their validity. Valid accounts are saved to `working-mc.txt`.

- **2. Generate Email and Password**: Generate random email and password combinations based on your specified quantity. The combinations are saved to `unchecked-mc.txt`.

- **3. Exit**: Exit the tool.

## File Locations

- `unchecked-mc.txt`: This file contains the email and password combinations to check or newly generated combinations.
- `working-mc.txt`: This file contains valid Minecraft account credentials.

