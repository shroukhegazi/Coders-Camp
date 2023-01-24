# Coders-Camp
<!-- GETTING STARTED -->
## Getting Started

This project is a small commuinty for coders to help them to learn more about programming concepts .

### How to run the project

1. You should have docker and docker-compose installed
2. Clone the repo
   ```sh
   git clone https://github.com/shroukhegazi/Coders-Camp/
   ```
3. Go in directory at the same level of docker-compose
 
4. Build images
   ```sh
   docker-compose build 
   ```
5. Migrate models
   ```sh
   docker-compose run web python3 manage.py migrate
   ```
6. Run the project
   ```sh
   docker-compose up
   ```








