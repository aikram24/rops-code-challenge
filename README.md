# rops-code-challenge

This repo contain the script to launch following AWS resources:
* VPC
* Subnet
* SG
* Instance

## Prerequisites
* Set your AWS profile to work with `eu-central-1` region
* Python2.7
* pip2.7


## How to run it
It will be prefer to run this in virtualenv so dependencies for this script don't have any conflict with existing libs.
You can run following commands in same order to execute the script:
```
$> mkdir ~/rops-env  # create a directory anywhere on your system
$> virtualenv -p $(which python2.7) ~/rops-env/venv
$> source ~/rops-env/venv/bin/activate
$> pip install git+https://github.com/aikram24/rops-code-challenge.git
$> deactivate && source ~/rops-env/venv/bin/activate   # it will de-activate and re-activate the virtualenv so you can start using newly installing script
$> rops
```


## Available Options
```
usage: rops [-h] [-k KEYNAME] [-a AMI] [-i INSTANCETYPE]
ReactiveOps Coding Challenge
optional arguments:
  -h, --help            show this help message and exit
  -k KEYNAME, --keyname KEYNAME
                        SSH Key Name
  -a AMI, --ami AMI     AMI ID (only ubuntu ami id)
  -i INSTANCETYPE, --instancetype INSTANCETYPE
                        Instance Type
```