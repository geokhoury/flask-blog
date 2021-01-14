# MongoDB on Docker

This project has a Docker Compose stack meant for development purposes.

## Prerequsites

To run this stack you need the following installed on your machine:

* [Docker Engine](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/install/)

## Stack

The stack contains two containers:

* **MongoDB** (uses the image `mongo:latest`) -- Runs the MongoDB community server.
* **Mongo Express** (uses the image `mongo-express:latest`) -- Runs a Node.js application to help manage your MongoDB.

## Running the Stack

On a Linux based operating system you can run the following:

* To start the stack

```bash
cd flask_blog/
docker-compose up -d
```

* To stop the stack

```bash
docker-compose down # to keep the data volumes
docker-compose down # to remove the data volumes
```

* To view the stack logs

```bash
docker-compose logs -f
```


## Standalone MongoDB Installation

If you do not wish to use Docker to run MongoDB, or if you run into issues you can additionally install MongoDB on your machine, and use MongoDB Compass to manage the server.

* [MongoDB Community Server](https://www.mongodb.com/try/download/community)
* [MongoDB Compass](https://www.mongodb.com/try/download/community)