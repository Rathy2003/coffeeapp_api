# COFFEE APP API
The **Coffee Shop API** is a backend service used to managing coffee shop digital (Web or Mobile App).
it provides a set of RESTFUL endpoint build with flask and mysql to handle core features such as:
- Category Management: create and organize product categories like (Americano, Expresso...).
- Product Management: create, update and retrieve coffee shop products with image, price, title...

### Installation
___
Step 1 : Create .env and config following
```
# Database Config
MYSQL_USER=your_usename
MYSQL_PASSWORD=your_password
MYSQL_ROOT_PASSWORD=your_mysql_root_password
MYSQL_DATABASE=your_database
MYSQL_HOST=your_host

# Secret Key
SECRET_KEY=your_secret_key
```

Step 2 : build docker image and run container\
```docker-compose up -d --build```

Step 3 : run migration file to create table\
``docker-compose run --rm web flask db upgrade``

### Usage
___

**Manage Category and Product**
- go to http://127.0.0.1:5000/admin
- login with user: ``admin`` and password: ``admin``
- will see **Category** and **Product** in menu