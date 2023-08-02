# docker notes cheatsheet


this is the first custom image I will try to to create a docker container for, so docker cheat sheet notes are contained here

# what is docker?

docker is a virtualisation software.
in a generic OS, there is an application layer, and a kernel.  The kernle is the middle man between the application layer and the hardware. It manages memory, cpu and threads.

### docker vs virtual machine
Virtual machines will create both an abstract application layer AND a virtual kernel. So the iamges take up quite a lot of diskspace, and take a buit to load.
Docker images on the other hand only anstract the application layer and use the host's kernel to operate. They boot up faster and take up a lot let space.
Initially they were created for linux (so a docker image could not run on windows because it was expecting to find a linux kernel and not a linux one but this has been changed)

Docker is great because different parts of an application can be packaged into an image, for every developer to install on their environment with a universla command, as opposed to doing this in the old fashioned way, where for an app each service needed to be installed differently depending on the developer's environment/

Docker thus makes the process of deploying applications and testing them a lot less error prone. Truly one procedure to follow that works on every env.

## docker images vs containers
a docker container is a running instance of a docker image.

Images are created and pushed to a registry, where developers can pull them down and work with them. The official docker registry is called "dockerhub". Unless you specify a different registry to look in, when you pull an image docker will automatically look there first.

You don't need an acc on dockerhub to pull down their images

## some quick docker commands to:

-to pull an image from dockerhub: (unless the version is specified docker will pull the latest image)
 <code>docker pull {name of image}:{version}</code>

- to view downlaoded local images:
<code> docker images</code>

 - to run a docker image:
 <code>docker run {name of image}:{version}</code>

 this will occupy a whole terminal session. To runa  docker image but have that terminal session free run: (the -d is used to run in detached mode)
<code>docker run -d {image name}:{version}</code>
the output returned is the id of the container running

- to view running local containers (processes)
<code>docker ps</code>
![image info](docker.png)

-to view logs of a specific running container:
<code>docker logs {CONTAINER ID}</code>

so following from the above example the command would be <code>docker logs a51e21e7d79d</code>

