#!/bin/bash
# postgres-setup.sh - Script to set up PostgreSQL in Docker for Modax Calculator

# Colors for prettier output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Configuration variables
DB_NAME="modax_calculator"
DB_USER="postgres"
DB_PASSWORD="12345"  # Change this to your desired password
DB_HOST="localhost"
DB_PORT="5432"
CONTAINER_NAME="modax-postgres"

# Print initial message
echo -e "${GREEN}=== Setting up PostgreSQL Docker Container ===${NC}"

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Docker is not installed. Please install Docker first.${NC}"
    exit 1
fi

# Check if PostgreSQL container is already running
if docker ps | grep -q $CONTAINER_NAME; then
    echo -e "${YELLOW}PostgreSQL container already running.${NC}"
    
    # Print credentials
    echo -e "${GREEN}=== Database Credentials ===${NC}"
    echo -e "${YELLOW}dbname: ${DB_NAME}"
    echo -e "user: ${DB_USER}"
    echo -e "password: ${DB_PASSWORD}"
    echo -e "host: ${DB_HOST}"
    echo -e "port: ${DB_PORT}${NC}"
    exit 0
fi

# Check if container exists but is not running
if docker ps -a | grep -q $CONTAINER_NAME; then
    echo -e "${YELLOW}PostgreSQL container exists but is not running. Starting container...${NC}"
    docker start $CONTAINER_NAME
else
    # Create PostgreSQL container
    echo -e "${GREEN}Creating PostgreSQL container...${NC}"
    docker run --name $CONTAINER_NAME \
        -e POSTGRES_PASSWORD=$DB_PASSWORD \
        -e POSTGRES_DB=$DB_NAME \
        -p $DB_PORT:5432 \
        -d postgres:13
fi

# Check if container was started successfully
if docker ps | grep -q $CONTAINER_NAME; then
    echo -e "${GREEN}PostgreSQL container started successfully!${NC}"
else
    echo -e "${RED}Failed to start PostgreSQL container.${NC}"
    exit 1
fi

# Wait for PostgreSQL to initialize
echo -e "${YELLOW}Waiting for PostgreSQL to initialize...${NC}"
sleep 5

# Print credentials
echo -e "${GREEN}=== Database Credentials ===${NC}"
echo -e "${YELLOW}dbname: ${DB_NAME}"
echo -e "user: ${DB_USER}"
echo -e "password: ${DB_PASSWORD}"
echo -e "host: ${DB_HOST}"
echo -e "port: ${DB_PORT}${NC}"

echo -e "${GREEN}=== Container Information ===${NC}"
docker ps | grep $CONTAINER_NAME

echo -e "${GREEN}=== Connection String Example ===${NC}"
echo -e "postgresql://${DB_USER}:${DB_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME}"

echo -e "${GREEN}=== Python Dict Format ===${NC}"
echo "DB_CONFIG = {"
echo "    'dbname': '${DB_NAME}',"
echo "    'user': '${DB_USER}',"
echo "    'password': '${DB_PASSWORD}',"
echo "    'host': '${DB_HOST}',"
echo "    'port': '${DB_PORT}'"
echo "}"