# Assignment 3

## FastAPI: 

* To build and run the docker container, first `cd ./code/fastapi`

* To build the Docker image from the Dockerfile:

    ```
    docker build -t my-fastapi-app .
    ```

* To create and start a Docker container based on the Docker image built above: 

    ```
    docker run -d -p 8000:8000 --name my-fastapi-container my-fastapi-app
    ```

* Then navigate to http://127.0.0.1:8000/ to see the launched app. We will however interact with spaCy through the command line: 

    * For general info: 

        ```
        curl http://127.0.0.1:8000
        ```

    * **NER parsing** (you can change the text you want to parse by editing the file `./code/fastapi/input.json` and `./code/fastapi/input.txt`):

        * for Windows:

        ```
        Invoke-RestMethod -Uri http://127.0.0.1:8000/ner -Method Post -Headers @{"Content-Type"="application/json"} -InFile input.json | ConvertTo-Json -Depth 100 | Out-Host
        ```

        * for Mac/Linux: 

        ```
        curl http://127.0.0.1:8000/ner -H "Content-Type: application/json" -d@input.txt
        ```

    * **DEP**: 

        * for Windows:

        ```
        Invoke-RestMethod -Uri http://127.0.0.1:8000/dep -Method Post -Headers @{ "Content-Type"="application/json" } -InFile input.json | ConvertTo-Json -Depth 100 | Out-Host
        ```

        * for Mac/Linux: 

        ```
        curl http://127.0.0.1:8000/dep -H "Content-Type: application/json" -d@input.txt
        ```


* To stop the container, first locate its ID by printing all active containers through the command line: 

    ```
    docker ps
    ```

* Locate the ID of the container you want to stop and/or remove (note that you must stop a container before you can remove it), then: 

    ```
    docker stop container-id
    docker rm container-id
    ```
## Flask App:

* To build the Docker image from the Dockerfile:

```
docker build -t my-flask-app .
```

* To create and start a Docker container based on the Docker image built above: 

```
docker run -d -p 5000:5000 --name my-flask-container my-flask-app
```

* Navigate to: http://127.0.0.1:5000/

## Streamlit App: 

* To build the Docker image from the Dockerfile:

```
docker build -t my-streamlit-app .
```

* To create and start a Docker container based on the Docker image built above: 

```
docker run -d -p 8501:8501 --name my-streamlit-container my-streamlit-app
```

* Navigate to: http://localhost:8501/


## Troubleshooting: 

* In case you cannot build your image or run your Docker container, first check if your container is running: 

    ```
    docker ps 
    ```

* If you cannot see your container in the list of active containers above, check its status by running the below command. If the status is "EXIT", this means there was an error while building your Docker image.

    ```
    docker ps -a
    ```

* Check the logs for full details on the error: 

    ```
    docker logs container-id
    ```






