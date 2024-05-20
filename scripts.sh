#!/bin/bash


# Build the image
et-build()
{
    docker compose -f docker-compose.yml build
}

# Run the container
et-up()
{
    docker compose -f docker-compose.yml up -d
}

# To take down the container
et-down()
{
    echo "Stopping the containers.."
    docker compose down --remove-orphans &> /dev/null
    echo -e "\033[92mContainers Stopped successfully!\033[m"
}

# Run flask server
et-run()
{
    et-down
    et-build
    et-up
    docker compose -f docker-compose.yml run --rm web python -m flask run --debug

}

# Access interactive shell
et-shell()
{
    et-down
    et-build
    et-up
    docker compose -f docker-compose.yml run --rm web bash

}