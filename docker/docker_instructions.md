## Add Your User to the Docker Group

`usermad -aG docker <username>`

### Refresh your group membership

#### Two ways

1. Log out and back in
2. Use the command `newgrp docker`

## Initial Install of Docker Container

### Command to install and run AVD all-in-one Docker container

`docker run --rm -it -v $(pwd):/home/avd/projects/ ghcr.io/arista-netdevops-community/avd-all-in-one-container/avd-all-in-one:latest`

### Breaking down the above command

`docker run`: Run the Docker container in manner prescribed by the following options

`--rm`: When this container is exited, remove it from the list of containers

`-it`: Start the container with an interactive terminal, i.e. a CLI with which you can interact

`-v`: Map a volume, linking a folder within the container with a folder on the machine running the Docker container

`$(pwd):/home/avd/projects`: This is the volume mapping - the present working directory (pwd) is mapped to /home/avd/projects within the container

`ghcr.io/arista-netdevops-community/avd-all-in-one-container/avd-all-in-one:latest`: This is the container that will be pulled down from the GitHub Code Repository and run

## Create an Alias to Run the Container

### In your user home directory (~/) open or create the .bashrc file in VI or VSCode and add the following line:

`alias avd='docker run --rm -it -v $(pwd):/home/avd/projects/ ghcr.io/arista-netdevops-community/avd-all-in-one-container/avd-all-in-one:latest'`

### Save the file

### Source the file

`source .bashrc`

!!! Note If your shell environment is something other than bash, replace the .bashrc file with the appropriate file for your shell, .zshrc for ZSH shell, for example

### Now to run the container, simply run the command `avd` and it will run the container and, if not found locally, download and run it

## Upgrade to a Newer Version of the AVD All-In-One Container

### Check which version of AVD you are running (run this command from while the container is running)

```sh
$ ansible-galaxy collection list

# /home/avd/.ansible/collections/ansible_collections
Collection        Version
----------------- -------
ansible.netcommon 5.1.2
ansible.utils     2.10.3
arista.avd        4.3.0  <-- AVD version
arista.cvp        3.8.0  <-- CVP role version
arista.eos        6.0.1
community.general 7.3.0
```

### Remove the current version and install the new one (exit the container and do this on the host)

```sh
$ docker images

REPOSITORY                                                                   TAG       IMAGE ID       CREATED        SIZE
ghcr.io/arista-netdevops-community/avd-all-in-one-container/avd-all-in-one   latest    c3ad82702a48   2 months ago   866MB

# Note the Image ID - only need to reference enough of it to be unique, usually no more than 4 digits

$ docker rmi c3ad

Untagged: ghcr.io/arista-netdevops-community/avd-all-in-one-container/avd-all-in-one:latest
Untagged: ghcr.io/arista-netdevops-community/avd-all-in-one-container/avd-all-in-one@sha256:123460283974c2c76479c08bc8ab84bced504a62b299e51aec17f740a805880b
Deleted: sha256:c3ad82702a488a2082f7f029c2157bcfef1cecaad755a6f1fd0c8ec6eaea226f
Deleted: sha256:ea8b5f1390b6ece7d6b00e3e23c01535ed371993ef4154372cf7b7ed98bf2e3c
Deleted: sha256:fd1c329ebfc0fdc091782b0817be4d74245c2d7debe2195184a4d2ec5d81255c
Deleted: sha256:6fa9c6367f0ba80c079a5baf062d7f42e5ee058e7a4fc0fde152482bf2cce186
Deleted: sha256:7022df8062c8f7826273624002dcb40914ab3788a4aa119c288ef42beaf06735
Deleted: sha256:7f771ffbcfc3fedc9bc51ccf0e0bd8342fd886c8ba7702b7feefe3acd9cd465e
Deleted: sha256:9e218d09d27914fd0ee40b728bf395eb547ac901cc19979b5951307e34099454
Deleted: sha256:f05a3d2db32f812663304762c4b19eb8ab5207e4f68edd85704bf5451436cf93
Deleted: sha256:a4c3ae08447ac28b6e224b11cbfe27132e2b6514638bef6a79f9d95d6642e2d8
Deleted: sha256:0b557cce986e7e87b48eca6343d85df9015faad98a0d2162a51521ac65ad03ba
Deleted: sha256:bdd32fc97454609c692ca7ad3025d2e68b0e1344ab16090edbafe0019eb6dc95

# Now just rerun the avd command and it will download and run the latest image

$ avd
```

![AVD command](./avd_command.gif)

### Verify the new version (back in the container)

```sh
$ ansible-galaxy collection list

# /home/avd/.ansible/collections/ansible_collections
Collection        Version
----------------- -------
ansible.netcommon 5.3.0
ansible.utils     2.11.0
arista.avd        4.4.0  <-- Updated version installed
arista.cvp        3.8.0
arista.eos        6.2.1
community.general 8.0.1
```
