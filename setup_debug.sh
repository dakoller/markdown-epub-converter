#!/bin/bash
# Setup script for debugging the Markdown to EPUB converter

# Print colored output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Setting up debugging environment for Markdown to EPUB converter...${NC}"

# Create test_output directory if it doesn't exist
if [ ! -d "test_output" ]; then
    echo -e "${GREEN}Creating test_output directory...${NC}"
    mkdir -p test_output
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Created test_output directory${NC}"
    else
        echo -e "${RED}✗ Failed to create test_output directory${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓ test_output directory already exists${NC}"
fi

# Make test_api.py executable
echo -e "${GREEN}Making test_api.py executable...${NC}"
chmod +x test_api.py
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Made test_api.py executable${NC}"
else
    echo -e "${RED}✗ Failed to make test_api.py executable${NC}"
    exit 1
fi

# Check if pandoc is installed
echo -e "${GREEN}Checking if pandoc is installed...${NC}"
if command -v pandoc &> /dev/null; then
    PANDOC_VERSION=$(pandoc --version | head -n 1)
    echo -e "${GREEN}✓ Pandoc is installed: ${PANDOC_VERSION}${NC}"
else
    echo -e "${YELLOW}⚠ Pandoc is not installed on the host system${NC}"
    echo -e "${YELLOW}  This is OK if you're using Docker, as pandoc is installed in the container${NC}"
fi

# Check if Docker is running
echo -e "${GREEN}Checking if Docker is running...${NC}"
if command -v docker &> /dev/null; then
    if docker info &> /dev/null; then
        echo -e "${GREEN}✓ Docker is running${NC}"
    else
        echo -e "${RED}✗ Docker is installed but not running${NC}"
        echo -e "${YELLOW}  Please start Docker to use the containerized version${NC}"
    fi
else
    echo -e "${YELLOW}⚠ Docker is not installed${NC}"
    echo -e "${YELLOW}  You'll need to install pandoc locally to use the application without Docker${NC}"
fi

# Check if docker-compose is installed
echo -e "${GREEN}Checking if docker-compose is installed...${NC}"
if command -v docker-compose &> /dev/null; then
    COMPOSE_VERSION=$(docker-compose --version)
    echo -e "${GREEN}✓ docker-compose is installed: ${COMPOSE_VERSION}${NC}"
else
    echo -e "${YELLOW}⚠ docker-compose is not installed${NC}"
    echo -e "${YELLOW}  You'll need docker-compose to run the containerized version${NC}"
fi

echo -e "\n${GREEN}Setup complete!${NC}"
echo -e "${YELLOW}To run the test script:${NC}"
echo -e "  ./test_api.py --url http://localhost:8088"
echo -e "\n${YELLOW}To build and start the Docker container:${NC}"
echo -e "  docker-compose up --build -d"
echo -e "\n${YELLOW}To view logs:${NC}"
echo -e "  docker-compose logs -f markdown-epub-api"
echo -e "\n${YELLOW}For more debugging information, see DEBUG.md${NC}"
