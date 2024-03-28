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




