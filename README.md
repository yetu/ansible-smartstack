# ansible-smartstack
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
 * Nerve checks the services(e.g. postgresql server) that you want and announces to serf, whether it is working or not.
 * Serf communicates this information to the other nodes via gossip protocol
 * Synapse figures out which services(e.g. postgresql server) are running and configures HAProxy for load balancing (e.g. postgresql client) 

That means, Serf is required both for nerve and synapse and Haproxy is required only for synapse





## Requirements
This role is tested with ubuntu 12.04 and ansible 1.7



## Role Variables
Please check following files for variables
	
	default/main.yml
	vars/services.yml


## Usage
Installation of synapse and nerve are have to be explicitly stated in your playbook.

	nerve_install           : True

If you would like to install synapse

	synapse_install         : True


You also have to give the list of your services that you want it to be available, for instance if you would like to 

	selected_services       : [ "postgresql" ]

You also need to define the services that you need, an example how services can be defined can be found at 

	vars/services.yml

Once you define your services you can give the path of your service file as a variable to the this role:

	smartstack_services_files  : "my-services.yml"


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
```sudo service serf stop``` then ```serf members```

### Simulate postgresql faliure 
on demo2  ```sudo service postgresql stop``` then head to http://192.168.56.151:3212/

## License
MIT

## Contributors (sorted alphabetically)
* [Adham Helal](https://github.com/ahelal)
* [Engin Yoeyen](https://github.com/enginyoyen)
