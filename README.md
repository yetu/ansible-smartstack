# ansible-smartstack


An ansible role that installes airbnb smartstack. For more info on [smartstack](http://nerds.airbnb.com/smartstack-service-discovery-cloud/)
This role uses the [getyourguide](https://github.com/getyourguide) smartstack fork.  The role will use serf instead of zookeeper.

## Requirements
This role is tested with ubuntu 12.04 and ansible 1.7

## Role Variables

check default/main.yml
check vars/services.yml

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
[http://192.168.56.151:3212/]

### Simulate failure serf failure
```sudo service serf stop``` then ```serf members```

### Simulate postgresql faliure 
on demo2  ```sudo service postgresql stop``` then head to [http://192.168.56.151:3212/]

## License
MIT

## Contributors (sorted alphabetically)
* [Adham Helal](https://github.com/ahelal)
* [Engin Yoeyen](https://github.com/enginyoyen)
