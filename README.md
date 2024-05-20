# Ensofia task

Develop a Dockerized Python project that accepts necessary parameters to process a payment using Authorize.Net payment gateway.

## Prerequisites

- WSL (For non-unix users)
- Docker

## clone this repository

- Open your terminal in your home directory (Optional location).
- Create a `src` directory to contain the project
  - mkdir src && cd src
  - clone the repository

## Docker Scripts Setup (One Use)

1. Run `source scripts.sh`.
2. Stay in the same terminal to be able to access docker shell commands.

## Docker Scripts Setup (Permenant)

1. Make sure your docker is installed and the daemon is running
   - By running: `docker ps`
2. Set environment variables in your ~/.profile or ~/.bash_profile:
   ```
   export ET_DIR="{the absolute path to the repo}"
   ```
   Example: `/home/user/src/ensofia-task`
3. Open new terminal to load the new variable
4. Load docker shell commands
   - Go to the project root directory and run `source scripts.sh`
   - Or you can add `source ${ET_DIR}/scripts.sh`to your ~/.bash to have the commands always available.

## Project Setup

Once shell commands are loaded, you can now use them to set and run the project in this order:

1.  create `.env` file by running `cp sample.env .env` and fill it with you credintials.
2.  `et-build`: to build docker container from image.
3.  `et-up`: to run the container
4.  `et-run`: to run flask server
5.  `et-down`: Once you are done with the container you can use this command to take it down (recommended to save your computer resources).
