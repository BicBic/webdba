#!/bin/bash -e
# Loop forever (until break is issued)
while true; do
	date
	sudo ssh -i linuxaws.pem -N -D 8666 ec2-user@ec2-54-243-15-147.compute-1.amazonaws.com
	sleep 10
done

