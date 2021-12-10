**ETL stocks microservices**

Microservices to get stock historical data from external source, like API or WebScrapy, transform and return to stock microservices https://github.com/mborcari/stock_microservices

It currently supports infomoney and yahoo finance.

**Stack of project:**

- Pyenv and virtualenv for management environment;
- Docker and Docker-compose;
- Pike, RabbitMq;

You will need install git, heroku and docker CLI.

Login in Heroku and Docker in console.

```
heroku login
heroku container: login
```

Here, you will create two stock etl microservices

**Warning: Remember! change tag "yourname" on this read-me!.

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
  
  
  Use this command to see the log on continer:
   ```
    heroku logs --tail -a ms-etl-1-yourname
   ```
