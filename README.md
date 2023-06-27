# Creating and Activating a Virtual Environment and run the program


To create a virtual environment for your project, follow these steps:


1- Open a command prompt and navigate to your project directory.


2- Run the following command to create a virtual environment named "env":

```python
python -m venv env
```


3- Activate the virtual environment by running the appropriate command based on your operating system:

  - For Unix/Linux/macOS:
    ```python
    source env/bin/activate
    ```

  - For Windows:
    ```python
    ./env/Scripts/activate
    ```


4- Install dependencies required to run the program correctly. At the root folder, run the command line:

```python
pip install -r requirements.txt
```


5- execute main file to run the program:

```python
python ./main.py
```


6- When you're done working within the virtual environment, you can deactivate it by running:

```python
deactivate
```