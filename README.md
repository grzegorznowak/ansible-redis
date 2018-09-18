# Ansible Role: Redis


Installs [Redis Server](https://redis.io/) on Debian.

Minimalistic version of a multi-config redis role for debian-based distreos, with tight test coverage using molecule 
(so you can test locally with minimal effort) and a docker compatible layer if you wanted to build it on top of a docker container.

It will create separate config files (located under /etc/redis/redis-{{name}}.conf), as well as stand-alone /var/log/redis/ 
logging points for each config defined.

The role is perfect for dev purposes to test multiple configurations on a single machine, as well as for live deployments
with it's minimalistic fully-molecule-covered and linted code.  

Leverages `systemctl` on lxd/baremetal and simple `init.d` on docker. 

## Requirements

No dependencies.

## Coverage

Currently builds and integrates on latest debian-based distros:

##### Ubuntu: 18.04, 16.04
##### Debian: buster, stretch

 

## Variables

### defaults
    redis_package_name: "redis-server"  
    
    redis_configs:
      - port: 6380      # port to listen on   
        name: "cache"   # configuration name - will also affect logfile (/var/log/redis) and pidfile target names
        bind: 127.0.0.1 # which ip to bind to (localhost being the safest option for self-service)
        
### a sample multiconfig

    redis_configs:
      - port: 6379,
        name: "cache"
        bind: 127.0.0.1   
      - port: 6380,
        name: "session"
        bind: 127.0.0.1
      - port: 8080,
        name: "shared-cache"
        bind: 0.0.0.0  
        # beware the last one will open up 8080 to the outside world, 
        # so will need a separate hardening rules (not included in this role)        
        

Currently the role installs whatever latest stable version lives in supported distros' upstreams.         

## Example playbook 
##### when cloning from github

    ---
    - hosts: all
      vars:
        redis_configs:
          - port: 6379,
            name: "cache0"
            bind: 127.0.0.1
          - port: 6380,
            name: "cache1"
            bind: 127.0.0.1
      roles:
        - role: ansible-redis
        
##### when from ansible-galaxy

    ---
    - hosts: all
      vars:
        redis_configs:
          - port: 6379,
            name: "cache0"
            bind: 127.0.0.1
          - port: 6380,
            name: "cache1"
            bind: 127.0.0.1
      roles:
        - role: grzegorznowak.redis        

## Testing

### Requirements

* https://molecule.readthedocs.io/en/latest/installation.html
* [specific molecule LXD install doc](molecule/default/tests/INSTALL.rst)
* [specific molecule docker install doc](molecule/docker_dev/tests/INSTALL.rst)



### Testing with low-level LXD chroot containers

    molecule test

### Testing against docker base images

    molecule test --scenario-name=docker_dev

### Additional perks from molecule

Remember you can also do crazy stuff like `molecule converge` to simply bring instance(s) at will and then tear them down
with `molecule destroy`. The sky is the limit here really!

## Sponsored by

#### [Kwiziq.com](https://www.kwiziq.com) - The AI language education platform
#### [Spottmedia.com](http://www.spottmedia.com) - Technology design, delivery and consulting


## Author Information

made with love by [Grzegorz Nowak](https://www.linkedin.com/in/grzegorz-nowak-356b7360/).
