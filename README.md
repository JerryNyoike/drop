# Drop
This project aims to create an online marketplace for budding music producers where they can get a bigger market reach.

## Technologies used
1. Python
2. Flask

## Techniques used
1. Machine Learning. We take advantage of machine learning to predict music genres and also to predict user tastes so that we can recommend to them more of what they will enjoy. The aim of this is to increase sales for producers.

## Directions on Running the Notebook
1. Clone the repository git clone https://github.com/JerryNyoike/askfortransport.git
2. Install
    - [Python](https://www.python.org/downloads/)
    - [MySQL](https://dev.mysql.com/doc/refman/8.0/en/installing.html)

3. Set up a [virtual environment](https://docs.python.org/3/tutorial/venv.html) in the root folder of the project using the command `python3 -m venv .` while inside the project folder.
4. Install project dependencies using [pip](https://pip.pypa.io/en/stable/installing/) by executing the command `pip3 install -r requirements.txt` when inside the root directory.
5. Create a database instance using the command `mysql source app/schema.sql` from the project's root directory.
6. Run the Flask server with the commands 
    ```
    $export FLASK_ENV=development
    $export FLASK_APP=lig.py
    $flask run
    ```

## Contributors
[Braxton Muimi](https://github.com/Brackie)

[Jerry Nyoike](https://github.com/JerryNyoike)
