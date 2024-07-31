# sudoku-gui-solver

## Overview

This is a small and fun side project I created to visualize the capabilities of a backtracking algorithm in solving a sudoku board.

I used pygame to be able to visualize the backtracking aspect of solving the board; a green cell represents a new added number and a red cell represents backtracking as a result of an invalid number being inserted prior in the board. 

## Running the Script

Run the following commands to clone the project and download any nessecary python libraries

```bash
git clone https://github.com/[project name]
```

Once we've successfully copied the repository, run the following commands

### In Windows

```bash
python -m venv venv
source venv/Scripts/activate
```

```bash
pip install -r requirements.txt
```

### In Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

```bash
pip3 install -r requirements.txt
```

Once we've setup the repository correctly, run the following command

### In Windows

```bash
python main.py
```

### In Mac

```bash
python3 main.py
```

## Using a custom board

To solve a 9x9 board other than the one provided, write into the `sudoku_board.txt` file. The board should be formatted into each line being a row of the board and each column of the board separated by a comma. Furthermore, notice that we use 0 to represent an empty cell. 

Notice that the board should be valid. Otherwise, you should expect undefined behavior. 
