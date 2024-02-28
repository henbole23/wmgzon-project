# WMGZON

WMGZON is an upcoming eCommerce site selling a variety of different products, from music to sports accessories. This project contains the source code for the website's phase 1 implementation. In its current format, this project offers a landing page, with recently added products displayed in a carousel. There are individual product category pages, accessed via a product bar. The site also features admin functionality as well as product sorting and filtering. Users are able to complete the entire journey through the page to checkout, although the checkout form does not currently link to the database. Speaking of which, this project uses SQLite to store all user and product data required for the website to run.

## Installation
To set this project up follow the steps below:

1. Ensure python is installed on your system
2. Request access to the project repository
3. Clone the repository
4. Install the requirements found in requirements.txt

    `pip install -r requirements.txt`

## Usage
- Run Application: 
    - Option A: Direct through Python
        1. Open a terminal/command prompt or chosen IDE
        2. Navigate to the project directory run.py file
        3. Either run the file run.py through the IDE or enter the following command in the terminal:

            `python run.py`
    - Option B: Docker Container
        1. Ensure Docker Desktop is installed on your system
        2. Open a terminal/command prompt
        3. Navigate to the project directory
        4. Run the following command:

            `docker build -t wmgzon:v1.0`
        
        5. Then to run the image as a container run the following command:

            `docker run wmgzon`

## Credits
Developed by student u5500520 for the SDLC WMGZON Assignment 2024

## Roadmap

- Phase 1 has been met and is currently in review

- Phase 2 of this of project will consist of an enhanced Inventory Management System leading in to a fully fledged Checkout System. Requirements are currently being realised.

## Contact

u5500520@live.warwick.ac.uk
