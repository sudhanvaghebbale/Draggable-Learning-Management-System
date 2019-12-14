# Steps to Run Flask Application.

## 1.Setting up Python with Anaconda Enviroment. 
* Download and install anaconda from ```https://www.anaconda.com/distribution/```

## 2.Fetching Project Files from GitHub.
* Clone our repo from GitHub from this link ```https://github.com/SER515-Team15/Project.git```
* Change Branch to Stable-Version-v2
* *(Note: We ran into some issues in the last moment with our master branch not loading some html files due to dependency issues so instead we are using this branch as our pseudo master. Inconvenience is deeply regreted!)*


## 3.Setting Up Flask and it's dependencies.
* Open the Annaconda Prompt using the start button.
* Navigate to the directory where the our project repository was cloned.
* Start a conda enviroment by the following command  ```conda activate myenv```
* After activating enviroment install Flask using Pip using this command ```pip install Flask```
* Install the database driver using this command ```pip install SQLAlchemy```


## 4.Setting up SQL database and making configuring the main.py file.
* Download and install  Mysql from here ```https://www.mysql.com/downloads/```
* After installing open the SQL query shell and execute the following query

```
CREATE DATABASE LoginRegister;
USE LoginRegister;
CREATE TABLE Users ( Name varchar(50) NOT NULL,
Email varchar(50) PRIMARY KEY,
Password varchar(50) NOT NULL,
Role varchar(50) NOT NULL,
Status int NOT NULL);

```
* Navigate to our repository directory and open main.py in an editor file. 
* Notice the following line
```
_engine = create_engine("mysql+pymysql://root:Sudhanva@localhost/LoginRegister")
```
* change it to 

```
_engine = create_engine("mysql+pymysql://root:Yourpassword@localhost/LoginRegister")
```
* Save the file

## 5.Runing the Applicaiton.
* Type ```python main.py``` to start the Flask server
* In the browser open ```http://127.0.0.1:5000/``` to see our home page. 
