# DeltaTask3
## 3a Submissions
Found inside the Tasks 3a folder, both the files to be run on the server and the client machines are given, along with the dockerfile and compose yaml file for running the whole thing as containers with a mysql database. 
Running the server.py file sets up a server socket that can
- recieve multiple clients
- updates leaderboard and useres to databases in mysql server
- can send and recieve strings and objects (dictionaries) for the QnA purposes.

To run the sql server in docker seperately while testing the python file, the following can be run in terminal

```
docker run --name mysql-db -e MYSQL_ROOT_PASSWORD=root -p 3333:3306 -d mysql:latest
```

