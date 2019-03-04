# social-cops

I have synced the data between two directories on Droid A and Droid B respectively. I have written a Dockerfile which provides the desirable environment to run the python script on each Droid. The python script runs a WATCHDOG which monitors any type of change that occurs in the particular directory of the Droid. The script also runs a MQTT client on each Droid to send data to the MQTT broker which is responsible for publishing data to its subscribers,  Droid A and Droid B in this case. In short, the monitoring of the directory in each Droid is achieved by python package WATCHDOG and the syncing of data between two Droids is achieved by MQTT.

How to run a solution on each Droid:-
1. To run the solution either OS should have Docker installed or the latest version of python should be installed.
2. Clone the code from Github repo https://github.com/imayushchauhan/social-cops which contain a Dockerfile and clone_war.py file
3. Update the path variable in clone_war.py which is basically store a path of the directory which you want to monitor.
4. Open terminal and Go to the code directory and Run        pip3 install -r requirements.txt && python3 clone_war.py        command to run the solution via python. 
4. Open terminal and Go to the code directory and Run        docker build -t clonewar . && docker run -d clonewar       command to run the solution via Docker.
5. Make any changes to the directory which you have defined in path variable such as create a directory or a file, modify a directory or a file, delete a directory or a file, move a directory or a file.
6. You were able to see the changes done to the directory in Droid A are reflected to the directory in Droid B.
