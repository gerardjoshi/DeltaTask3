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
## Forensics- steganography

Using kali-linux on arm64 meant compiling issues when running the file and execution errors like `file cannot be added` or `image not supported` even if format was supported. Hence stegosuite used for arm-compatibility.
following commands run:
```
stegosuite embed -m the message i want in the file -f samply.txt -o mystery.jpg -k mukund
```
Here, samply.txt is the text file to be embedded, mystery.jpg is the file into which it is embedded and mukund is the key phrase needed to extract the file back.
