# SpellWritingGuide

This is the tidier version of the code used in the [Spell Writing Guide](https://www.drivethrurpg.com/product/429711/The-Spell-Writing-Guide?manufacturers_id=22808) which aims to provide a simple method by which we can draw spells in D&D 5e. The system is general to any system and easy to modify, I will explain this later. 

# **!!! OLD REPO ALERT !!!**

**THIS IS RUBBISH**, or at least it's out of date.

[GO HERE](https://github.com/GorillaOfDestiny/SpellWriting) for a much nicer and more complete repo. I'm only keeping this active for those curious about the old methods of generating things.

## Setup

You can clone the repo for use simply by typing:

```git clone https://github.com/GorillaOfDestiny/SpellWritingGuide```

When initially running the code a folder called "Uniques" with files such as "11.npy" being created within. These contain the rotationally unique binary numbers the method relies on. They will only be created when such a file does not already exist in a directory called "Uniques".

### Dependencies

Python vesion used in development: Python 3.10.4

The required python modules are:
  - numpy
  - matplotlib
  - argparse
  - math
  - os
  - tqdm
 
## Running the file

to run you type the command: ```py writer.py```

for information about optional commands type: ```py writer.py --help```

standard input for a spell is ```py writer.py -level <level> -range <range> -area <area> -dtype <dtype> -school <school>``` with <value> replaced by relevant lowercase strings. Defaults to make "Fireball".
  
To see the available inputs (and their format) type:  ```py writer.py --arg_help -<arg>...```
  
input options are defined by the .txt files in "Attributes/" so ```--arg_help``` simply prints the values in this file.
  
## Modifying
  
You can add your own options to the inputs by adding them in a new line in the relevant .txt files in "Attributes/"
  
  

