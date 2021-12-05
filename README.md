**ETL stocks microservices**

Microservices to get stock historical data from extrenal source, like API or WebScrapy, transformation and return data.

**Stack used:**

- Use pyenv and virtualenv for management environment;
- Docker and Docker-compose;
- Pike, RabbitMq;

You will need install git, heroku and docker CLI.

Login in Heroku and Docker in console.

```
heroku login
heroku container: login
```
To aplication works, is need:

- 1x stock microservices. (https://github.com/mborcari/stock_microservices)
- 2x stock etl microservices (https://github.com/mborcari/stock_etl_microservices)
- 1x Postgres database instance.
- 1x RabbitMQ instance.

Here, you will create two stock etl microservices

**Warning: Remember change tag "yourname" in this readme!.

  **Heroku commands to create stock etl microservices:**
  
  Create apps containers:
  ```
    heroku create ms-etl-1-yourname
    docker build -f Dockerfile -t img_stock_ms_etl .
    docker tag img_stock_ms_etl registry.heroku.com/ms-etl-1-yourname/worker
    docker push registry.heroku.com/ms-etl-1-yourname/worker
    heroku container:release worker -a ms-etl-1-yourname
    heroku ps:scale worker=1 -a ms-etl-1-yourname

    heroku create ms-etl-2-yourname
    docker build -f Dockerfile -t img_stock_ms_etl .
    docker tag img_stock_ms_etl registry.heroku.com/ms-etl-2-yourname/worker
    docker push registry.heroku.com/ms-etl-2-yourname/worker
    heroku container:release worker -a ms-etl-2-yourname
    heroku ps:scale worker=1 -a ms-etl-2-yourname
  ```
  
  
  Use this command to see log on continer:
   ```
    heroku logs --tail -a ms-etl-1-yourname
   ```
