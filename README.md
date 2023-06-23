Creating and Activating a Virtual Environment and run the program


To create a virtual environment for your project, follow these steps:

- Open a terminal and navigate to your project directory.

- Run the following command to create a virtual environment named "env":

python -m venv env


Activate the virtual environment by running the appropriate command based on your operating system:

For Unix/Linux/macOS:
source env/bin/activate

For Windows:
.\env\Scripts\activate


Go back to root folder and install dependencies required to run the program correctly by running the command line:

pip install -r requirements.txt


execute main file to run the program:

python ./main.py


When you're done working within the virtual environment, you can deactivate it by running:

deactivate
