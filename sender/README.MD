### Telegram bot for sending images to recipients in Docker

#### Docker

**Install and run**

Download docker from [official site](https://www.docker.com/products/docker)

**Starting project**

Rename `docker-compose.yml.example` to `docker-compose.yml`

Set `TELEGRAM_API, MYSQL_DATABASE, MYSQL_USER, MYSQL_PASSWORD` with your data

Run docker-compose file:

```bash
docker-compose up -d
```

**Inisde docker-compose**

##### DB - MySQL container

MySQL database contains records about recipients

**Ports**

| Value         | Description  | 
| ------------- |:-------------:|
| 127.0.0.1:8765:3306  | Database publish mysql default port on loclahost:8765  |


**Environment**

| Value         | Description | 
| ------------- |:-------------:|
| TELEGRAM_API | Telegram API for our bot. Get this api with BotFather help|
| MYSQL_RANDOM_ROOT_PASSWORD | If set 'yes' container will generate random password|
| MYSQL_DATABASE | Database name for our projct |
| MYSQL_USER | User for database|
| MYSQL_PASSWORD | Password for MYSQL_USER |

**Volumes**

| Value         | Description  | 
| ------------- |:-------------:|
| /docker_storage/observe/db:/var/lib/mysql | Store database files on hardnode filesystem |
| /docker_storage/observe/status:/status | Directory for database ready status |
| /db/init.dump/:/docker-entrypoint-initdb.d | Directory for impotring dump |


##### Checker - Send meassages to Telegram

**Links**

| Value         | Description  | 
| ------------- |:-------------:|
| db:mysql  | Linking db as mysql for acees to database  |

**Ports**

| Value         | Description  | 
| ------------- |:-------------:|
| /docker_storage/observe/checker:/checker | Directory for upload images |
| /docker_storage/observe/status:/status | Checking MySQL status before start |




##### Bot - Telegram bot for management

**Links**

| Value         | Description  | 
| ------------- |:-------------:|
| db:mysql  | Linking db as mysql for acees to database  |

**Ports**

| Value         | Description  | 
| ------------- |:-------------:|
| /docker_storage/observe/status:/status | Checking MySQL status before start |

