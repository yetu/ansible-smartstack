# ansible-smartstack
[![Build Status](https://api.travis-ci.org/yetu/ansible-smartstack.svg?branch=master)](https://travis-ci.org/yetu/ansible-smartstack/)

SmartStack is an automated service discovery and registration framework. 
This ansible role installs airbnb smartstack, which includes following components

 * ruby
 * nerve : for service registration.
 * synapse : for service discovery. 
 * serf : for cluster membership
 * HAProxy : for load balancing 

For more information on [smartstack](http://nerds.airbnb.com/smartstack-service-discovery-cloud/)
This role uses the [getyourguide](https://github.com/getyourguide) smartstack fork.  
The role will use serf instead of zookeeper.

## How it Works
 * Assumption : There are two services, Service-A and Service-B. There are n numbers of Service-A which Service-B connects it.
 * Nerve run on every instance of Service-A and announces that service is up and running via serf
 * Serf communicates this information to the other members via gossip protocol
 * Synapse which runs on Service-B get this information from serf and and configures HAProxy
 * Service-B now can connect to list of Service-A. If there is a new instance of Service-A this will be added into the HAProxy.
 * If one of them fail will be removed from the HAProxy.
 

That means, Serf is required both for nerve and synapse and Haproxy is required only for synapse.


## Requirements
This role is tested with ubuntu 12.04 and ansible 1.7



## Role Variables
Please check following files for variables

	default/main.yml
	vars/services.yml


## Usage
Installation of synapse and nerve are have to be explicitly stated in your playbook.
```yaml	
	nerve_install           : True
```
If you would like to install synapse
```yaml	
	synapse_install         : True
```

You also have to give the list of services that you want to make available, for instance if you would like to announce the postgres service
```yaml	
	nerve_selected_services       : [ "postgresql" ]
```	
	
You also have to give the list of services that you want to connect to / use, for instance if you would like to connect to a memcache service running on another server:
```yaml	
	synapse_selected_services       : [ "memcache" ]
```
You also need to define the services that you need, an example how services can be defined can be found at 

	vars/services.yml

Once you define your services you can give the path of your service file as a variable to the this role:
```yaml	
	smartstack_services_files  : "my-services.yml"
```

## Example Playbook

Head to demo directoy
Requires Vagrant 1.5 +

```vagrant up``` Two vagrant images will be created 

demo1 (192.168.56.150)
- postgresql server
- nerv
- serf

demo2 (192.168.56.151)
- postgresql client
- synapse
- serf
- haproxy

###To check serf members
From demo1 or demo2 type  ```serf members```

###To check haproxy stats page
http://192.168.56.151:3212/

### Simulate failure serf failure
On demo1 type ```sudo service serf stop``` then on demo2 ```serf members```
enable back serf on demo1 by typing ```sudo service serf stop```

### Simulate postgresql faliure 
on demo2  ```sudo service postgresql stop``` then head to http://192.168.56.151:3212/

## License
MIT

## TODOs

* a service guarantee (runit, monit, ...)

## Contributors (sorted alphabetically on the first name)
* [Adham Helal](https://github.com/ahelal)
* [Engin Yoeyen](https://github.com/enginyoyen)
* [Joé Schaul](https://github.com/jschaul)
