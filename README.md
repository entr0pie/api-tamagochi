<p align="center"><img src="assets/tamagochi.gif" width="130"></p>
<h2 align="center">API-Tamagochi</h2>


> An API written in Flask for the Tamagochi application, an initiative of the research and development group at Universidade Positivo in the year of 2022/2023.

## Description

The Tamagochi application is an educational tool designed to assist children with their daily tasks through a virtual pet, similar to a Tamagochi. This repository contains only the API, without the graphical interface.

## Technologies Used

The following technologies and libraries were used in the development of this project:

- [Flask](https://flask.palletsprojects.com/en/2.3.x/quickstart/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Swagger UI](https://swagger.io/tools/swagger-ui/)
- [MariaDB](https://mariadb.org/)
- [JWT](https://jwt.io/)
- [Bcrypt](https://pypi.org/project/bcrypt/)
- [Nginx](https://www.nginx.com/)

## Installation (Docker)

To set up the project on your local machine, follow these steps:

1. Make sure you have [docker](https://docs.docker.com/engine/install/) and [docker compose](https://docs.docker.com/compose/install/) installed properly.
2. Clone this repository.
3. Inside the directory, run:

```
docker compose up --build
```

Access your [localhost](http://localhost).

4. (Optional) add the domains and subdomains to `/etc/hosts`

```
SERVER_ADDRESS=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' tamagochi-nginx-1)

echo "$SERVER_ADDRESS tamagochi.up.br" >> /etc/hosts
echo "$SERVER_ADDRESS parent.tamagochi.up.br" >> /etc/hosts
echo "$SERVER_ADDRESS child.tamagochi.up.br" >> /etc/hosts
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
