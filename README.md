<p align="center"><img src="assets/tamagochi.gif" width="130"></p>
<h2 align="center">API-Tamagochi</h2>


> An API written in Flask for the Tamagochi application, an initiative of the research and development group at Universidade Positivo in the year of 2022/2023.

## Description

The Tamagochi application is an educational tool designed to assist children with their daily tasks through a virtual pet, similar to a Tamagochi. This repository contains only the API, without the graphical interface.

## Technologies Used

The following technologies and libraries were used in the development of this project:

- Flask
- SQLAlchemy
- Swagger UI
- SQLite3
- JWT
- Bcrypt

## Installation

To set up the project on your local machine, follow these steps:

1. Clone this repository.
2. Enter in the `tamagochi` folder and install the project dependencies:

```
cd tamagochi 
pip install -r requirements.txt
```

3. Start the server: 

```
python3 main.py
```

4. (Optional) If you want to generate a new database, run:

```
sqlite3 -init database/source.sql database/tamagochi.db
```

Or through Python:

```
python3 -c "import sqlite3; sqlite3.connect('database/tamagochi.db').cursor().executescript(open('database/source.sql').read()).close()"
```

## Documentation

To see our current goals and more information about the project, visit our [Notion page](https://www.notion.so/Bichinho-virtual-c36336edc60b421b832e46b7d529ea31).

The API documentation can be accessed at [`/docs`](http://localhost:5000/docs). From there, developers can understand the available endpoints and their functionalities.

## Known Issues

As the project is still in its early stages of development, there may be known issues or limitations. 

## Future Plans

The following are the planned future enhancements for the project:

- [ ] Implement creation, editing, and deletion of tasks.
- [ ] Create a separate JWT for the "Child" user.
- [ ] Allow editing and deletion of the "Parent" and "Child" user.

## License

All the code in this and other repositories solely belongs to Universidade Positivo. All rights reserved.
