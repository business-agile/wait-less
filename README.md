# WaitLess 
![License](http://img.shields.io/:license-mit-blue.svg)

- There you have the classic `static/` and `templates/` folders. The `templates/` folder contains macros, error views and a common layout.
- `views/` folder to separate the user and the website logic, which could be extended to the the admin views.
- The same goes for the `forms/` folder, as the project grows it will be useful to split the WTForms code into separate files.
- The `models.py` script contains the SQLAlchemy code, for the while it only contains the logic for a `users` table.
- The `toolbox/` folder is a personal choice, in it you keep all the other code the application will need.
- Management commands should be included in `manage.py`. Enter `python manage.py -?` to get a list of existing commands.
- Makefile for setup tasks, it can be quite useful once a project grows.


### Virtual environment

```
pip install virtualenv  
virtualenv venv  
venv/bin/activate (venv\scripts\activate on Windows)  
make install    
make dev  
python manage.py initdb  
python manage.py runserver  
```



Thanks to https://github.com/MaxHalford for his boilerplate Flask project.
