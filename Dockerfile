##################################################################

FROM ubuntu:latest

ARG DEBIAN_FRONTEND=noninteractive

ENV TZ=America/Chicago

##################################################################
# Install necessary apt packages
##################################################################
 

RUN apt-get update && apt-get upgrade &&\
    apt-get install -yq --no-install-recommends apt-utils &&\
    apt-get install -yq build-essential git python python3 python3-pip bsdmainutils libboost-all-dev
 
RUN python3 -m pip install -U matplotlib scipy numpy z3-solver

WORKDIR /home
	


####################################################################
# Git Clone cgo2022 artifact
####################################################################
RUN git clone https://github.com/bpfverif/tnums-cgo22.git
WORKDIR /home/
