# Run hello.py
open terminal
Type >> python hello.py


# Run hello.py inside python vm
open terminal
type >> python -m venv mypyvm

# Add git ignore.

# To start vm
Type >> source mypyvm/bin/activate

# To stop
Type >> deactivate

# If you wanna install dependencies from requirements.txt,
# Run the following
Type >> pip3 install -r requirements.txt

# If you do not have, dependencies file, requirements.txt, create one as follows
Type >> pip3 freeze > requirements.txt

# Now run the script
Type >> python hello.py




