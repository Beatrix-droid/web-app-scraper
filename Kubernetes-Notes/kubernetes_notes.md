# Kubernetes Basics
This is intended to be a basics overview of Kubernetes, aimed at helping individuals first getting started with the tool. It is by no means exhaustive, as there is quite a steep learning curve to learn the tool.

### Outline of the guide:
- what is Kubernetes and why do we need it
- Kubernetes architecture
- main Kubernetes components
- hands on example

## What is Kubernetes?
Kubernetes is an open source container _orchestration tool_. It was originally developed by Google.

It helps you manage containerised applications that are made up of different containers in _different deployment environments_. (physical machines, virtual machines, cloud envornments, etc)

## What problems does Kubernetes solve and what are the tasks of an Orchestration tool?

The rise of _microservices_ caused an increased usage of container technologies (like Docker) because containers offer the perfect host for small independent applications like microservices.
This resulted into applications comprised of many containers. Managing those containers that an be in all sorts of environments with scripts or other self made tools can be really challenging and error prone.

This caused the demand for a _proper way_ of _managing_ those hundres of containers.

### What features do orchestration tools offer?
- high availability: app is always running, no downtime
- scalability or high performance
- disaster recovery: back up and recovery

## Kubernetes Architecture:
Kubernetes clusters are made up of _nodes_. A _node_ is a virtual or physical machine.
Each Kubernetes cluster is made up of one Master (main)node.
Then there are a couple of Slave (worker) nodes.
Each node has kubelet process running on it.
A _kubelet_ is a Kubernetes process that makes it possible for the cluster to talk to each other and execute some tasks on the nodes.

Each Slave node has containers of applications running on it. 
Slave/Worker Nodes are where the application is actually running.

The Master node runs several processes related to managing the cluster properly.

1. One such process is an API server which also is a container.
This API Server is the entrypoint to the K8s (Kubernetes) cluster.

2. There is also a Controller Manager. This keeps track of what is happening in the cluster. Checks if a container died, whether something needs to be repaired, etc etc.

3. Scheduler: ensures Pods replacement The Shceduler decides on which Node the new Pod should be scheduled based on the resources available on each node., and the load that that container needs.

4. etcs = Kubermetes backing store: holds at any point the current state of the Kubernetes cluster. The back up and restore mechanism uses this .

5. Virtual Network: spans all the nodes that are part of the cluster, and is what allows the nodes to talk to each other. It creates one unified machine.

Master nodes are crucial. If those go down you lose access to the cluster, so in production environments, there are usually more than one master nodes.


## Main Kubernetes Components
These are the main Kubernetes Components:

- Pod
- Service
- Ingress
- Deployment
- Secret
- ConfigMap
- StatefulSet
- DaemonSet

### Pod
The smallest unit in Kubernetes is called a _pod_.
A pod is an abstraction over a container. It creates a layer of abstraction over a container. This is needed because Kubernetes wants to abstract away the container runtime and technologies so that you can replace them if you want to, and so that you don't have to work with the container technology. (for ex, no need to interact with the docker technology or layer, just interact with the Kubernetes layer)

Each Pod gets its own Ip addres, required for that virtual network.

- Pods components are ephemeral, they can die very easily.
If a pod dies and gets respawned, the new pod gets a new IP address upon creation. This is not ideal if you are using IP addresses to communicate between pods, because once one dies you have to go and change the IPs in the scripts.


### Service and Ingress
Because of this, we have _Service (svc)_and _Ingress (ing)_
A _Service_ is a static, permanent IP address attached to each Pod.
The lifecycle of Service and Pod ARE NOT connected. So if the Pod dies, the IP of the service will stay.

If you want your app to be accessible via the browser, you'd need an _external service_. To prevent certain parts of your application to be accessible from the browser, you'd create an _internal service_.

You can specify the type of servuce upon creation.
Internal service is the default type.
![image info](Service.png)



_Ingress_ acts like a DNS, it forwards requests to the service, so that when visiting an app  in the browser, you don't have to type the IP address out.

### ConfigMap
External Configuration to your application. Will usually contain URLs to your application database, etc.
You just connect it to the pods. That way, if you change the name of the service, you jsut adjust the config map without having to change it everywhere else, rebuild images, etc...

ConfigMap is for non-confidential data only, as it is stored in plaintext.

### Secret
For sensitive configuration data (like passwords, credentials and tokens), Kubernetes has another component called _Secret_. It works just like the ConfigMap.
The data is stored in base64 encoded format.

The built in security mechanism is NOT enabled by default!
You are meant to encrypt it using a third party.

You can reference ConfigMap values or Seceret Values in a POd using environment variables or as a properties file.

### Volume (data persistence)
Imagine we have a database in a container. If the pod gets restarted the data would be gone.
We want the data to be persisted. This is achieved with _Volumes_.
The way this works is that it attaches a physical storage (like a hard drive) to your pod. It can be storage on the local machine, or remote outside of the K8s cluster.
![image info](volume.png)

Kubernetes doesn't manage data persistence! You are responsible for backing it up!

### Deployment 
In K8s we have multiple replicas of the same application so that if one replica dies, the app is still usable and reachable thanks to the other replicas.

In practice when a pod die, you don't recreate a new pod. Rather you create a _blueprint_ file called _deployment_ where you define the blueprint of the pod and specify how many replicas you want of it.

So deployments are an abstraction over pods and pods are an abstraction over containers.


### Stateful Sets
Databases cannot be replicated via deployemnts because they have states!
Pods would need to access the drive where the data is stored, meaning that we would have to create a management system that sess which pods are reading and writing to that storage in order to avoid inconsistencies.

This mechanism is offered by another Kubernetes component, called _Stateful Set_. It is meant specifically for database applications.Though typically you have a database application sitting outside a cluster, and you just have the cluster talk to it (so avoiding the stateful set, that can sometimes be difficult to configure.)


## Summarising the Main Kubernetes Components are:
- Pod, an abstraction of containers
- Service, used for communication
- Ingress Route traffic into cluster
- Config Map  external configuration that holds non-sensitive data
- Secret external configuration that holds sensitive data
- volumes : for data persistence
- blueprints for replicating pods with deployments and stateful sets (the latter uses for stateful applications like databases)

## Kubernetes Configuration
All the configuration in a Kubernetes cluster goes through a master node with a process called API server. This server is the trnypoint to the cluster. A Kubernetes client could be the kubernetes dashboard (available in the browser) or a client side script, or a command line tool like kubectl.
These API requests must be written in either YAML or JSON format. Here is a sample request:

```
metadata:
    name: my-app
    labels:
        app: my-app
spec:
    replicas: 2
    selector:
        matchlabels:
            app: my-app
    template:
        metadata:
            labels:
                app: my-app
        spec:
            containers:
                - name: my-app
                  image: my-image
                  env: 
                    - name: SOME_ENV
                      value: $SOME_ENV
                    
                  ports:
                    - containerPort: 8080
```
In this example request for deployment we instruct Kubernetes to create two replica pods for us called "my-app" with each pod replica having a container based on "my-image" running inside. In addition we configure the environment vairables and the port configuration.

The configuration requests in Kubernetes are _declarative_. We declare what our desired outcome is and Kubernetes will try and achieve that.


### Parts of a Configuration File
Every configuration file in Kubernetes has three parts:
1. Metadata (which includes name)
2. Specification (selectors, ports, you put every kind of configuration that you want to apply) (replicas, selector, template, ports ). The specifications vary depending on wether you are creating a service or a deployment.
3. Status: atuomatically generated by Kubernetes. Kubernetes will always compare the desired state with the actual state, and if they don't match Kubernetes knows that there is something to fix there, and it will try and fix it (self healing).
     And it will use the information from the etcs since it holds at any point the current state of the Kubernetes cluster.


## Production Cluster Setup
- Multiple master and worker nodes
- separate virtual or physical machines

### Test/Local Setup with minikube
- one node where both the master and the slave processes run. This node will have a docker container run time preinstalled

### Kubectl
Kubectl is a command line tool for Kubernetes cluster.
To talk to Kubernetes's API server you can use the Ui dashboard, the api or the cli (kubectl), which is the preferred way.

Sample commands to 
- create a local (test) cluster with minkube:
```minikube start --driver docker```
- ```minikibe status ``` will give us a status of the running nodes
- view the status of nodes:
```kubectl get node``:
![image info](get node status.png)

Minikube is for the start up/ deleting the cluster
whearas Kubectl CLI is for configuring the minikube cluster

# Sample Demo Kubernetes Build 
for this section see the files in the _Kubernetes Sample Config_ folder. This is a simple NodeJs app with a mongodb database
![image info](kubernetes-demo-app-diagram.png)
We will create 4 K8s configuration files for our Database:
- ConfigMap (MongoDB Endpoint)
- Secret (MongoDB User & Password)
- Deployment 
- Service   (deployment and service to create a MongoDB application with internal service)

2  Config files for the nodejs part of the app:
- Deployment 
- Service   (our own webapp with external service)


The service for the Mongodb database will be internal, whislt hte web app will be hosted with an external service so that users can visit it.
When creating config files it is always a good idea to reference the documentation and template config files which you can find by searching here:

_https://kubernetes.io_

## Creating the MongoDB ConfigMap:
(The complete code of this config Map can be found in _Kubernetes Sample Config/mongo-ConfigMap.yaml_)
We get a template Config Map from the documentation, and only copy part of it. We rename the name_key of under _"metadata"_ to _"mongo-app"_:

```
apiVersion: v1
kind: ConfigMap
metadata:
  name: mongo-database
data:
  mongo-url: mongo-service
```
thee _kind_ refers to what type of Kubernetes component this is (in this case a ConfigMap.) The medatadata/name key can be an arbitrary name, we've given it the name of "mongo-database" because it is configuring the mongo app that is part of our application

The _data_ field contains the actual contents, represented in _key-value pairs_.
There is a mongo-db url. This url will be the _Service name_ of MongoDB. Here it is called "mongo-service". We will create this service later.

## Creating the MongoDB Secret
(The complete code of this config Map can be found in _Kubernetes Sample Config/mongo-secret.yaml_)

```
apiVersion: v1
kind: Secret
metadata:
  name: mongo-secret
type: Opaque
data:
  MONGODB_USER: bW9uZ291c2Vy
  MONGODB_PASSWORD: bW9uZ29wYXNzd29yZA==
  ```

The kind this time is of type _Secret_, the metadata/name is again an arbitrary name (here named "mongo-secret") and the type is "Opaque", the _default_ for arbitrary key-value-pairs.

The username and passwords are encoded to base 64, we CANNOT set them in plaintext.
the "MONGODB_USER" username is "mongouser" which, encoded to base64 is "bW9uZ291c2Vy"
The "mMONGODB_PASSWORD" password is "mongopassword", which, encoded to base64 is: "bW9uZ29wYXNzd29yZA=="

Great, now that we have created the ConfigMap and Secret for MongoDB, these external configurations can be referenced in different deployments.

## Creating the MongoDb Deploy and Service Configurations
Now we will create the mongodb deployment and service configurations. They will both be contained in a single Yaml file called "Mongo.YAML". The file can be found at: _Kubernetes Sample Config/mongo.yaml_


### The deployemnt
```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: mongo-deployment
  labels:
    app: mongo
spec:
  replicas: 3
  selector:
    matchLabels:
      app: mongo
  template:
    metadata:
      labels:
        app: mongo
    spec:
      containers:
      - name: mongo
        image: mongo:5.0
        ports:
        - containerPort: 27017
```

There is also a spec key which contains deployment  specific specifications
as before we have the kind and metadata information.
- Kind "deployment" a bluepring for the pods
-metadata name: "mongo-deployment" (can be arbitrary)

Mainpart _Blueprint for Pods_
- template: configuration for Pod

The _template_ section has its own "metadata " and "spec" section
Within the configuration of the pod, we have the "containers" key.
 This can be a list of containers ( we have seen that pods can have multiple containers)
- In the "image" key define which image we will use in the pods.
In this case as we are configuring a deployment file for MongoDb we use the official mongodb image (pulled directly from dockerhub), with tag 5.0

- By default  Mongodb listens on Port 27017 so we set the container port to 27017

- We can also give the container a name, here we will call it "mongodb"

So  now we have configured the bluepring that creates pods with the mongodb image with version 5.0

Finally, we have _"labels"_ and _"matchlabels"_ in the file.
In Kubernetes you can give any component a label.
Labels are _key/value_ pairs that are attached to K8s resources. (anything can be labelled. COnfigmap, containers, pods etc...)

We also have _identifiers_ which should be meaningful and relevant to users:
example:
- "release": "stable"
- "env": "dev"
- "tier": "frontend"
- "release": "canary"
etc etc.

You can _identify_ and _address_ specific components using their labels.

- Labels DO NOT provide uniqueness. All Pod replicas will have the same label. WHy is this useful? But they all have their unique name

1. Connecting Deployment to all pod replicas

FOR PODS LABELS IS A REQURED FIELD

For other components like containers, deployment, configmap this is optional, but is good practice to include.

#### Label Selectors
How does deployment know which parts actually belong to it and how does Kubernetes know which pods belong to which deployment?

This is achieved with the _selector_ key and the _matchLabels_.

Selector match labels says that all the pods that match the label "app:mongo" belong to the deployment with the same label.

The slector will match the pods created with the configuration that has the same label.

The labels are completely up to you on how to define.

Finally there is the _replicas_ key which defines how many replicas we want to create from this bluebrint. In our case it will just be 1, because it is a database, and if you want to scale databases in Kubernetes you should use _Stateful Set_ and not a deployment


### The service:
immediately below the deployment code, we create another YAML document called "service"

```
apiVersion: v1
kind: Service
metadata:
  name: mongo-service
spec:
  selector:
    app: mongo
  ports:
    - protocol: TCP
      port: 27017
      targetPort: 27017
```
Again we have some metadata.
IMPORTANT: the NAME in the metadata is the ENDPOINT which we will use to access mongo in the configmap.
This is the name of the service.

The _selector_ attribute is important: it selects pods to _forward_ the requests to. We must connect service to Pods. How does Service know which pods belong to it and which ones it should forward the request to? Using the same label selector as we saw on deployment.

The selector label should match the same labels as the deployment labels of the pods.

In the _"ports"_ key we must map the container port from our _deployment_ to the _targetPort_, and the _port_ key can be arbitrary.
Much like  port binding with docker.
So here _targetPort_ is 27017. We will make the port key the same for simplicity

And this concludes our configuration for the MongoB part of the application!

Now Let's configure the WebApp and Deployment Service:

## Web App Config Files
For this we will just copy and paste the deployment and service configurations of mongodb into a new file and call it _"NodeWebapp.YAMl"_ and adjust accordingly.

First we change all the all the labels and label selectors from "mongo" to "webapp".
We do the same for the service.

Next we replace the mongodb image in the deployment part with the correct image.
In this case we can grab it from docker.
This is the image: nanajanashia/k8s-demo-app:v1.0

Finally we also change the port name. It starts at port 3000, so we will change the port in the deployment and service parts as well.


With this we have completed the basic configuration for deployment and Service for any application


## Pass Secret  and ConfigMap Data to Mongo 
We need to pass the Secret and ConfigMap Data into the pods.

When starting a mongodb application we need to set username and password.
When the app starts up these credentials will be generated so that we can access them when .

We can check how to configure credentials for mongodb upon startup by going onto the documentation:
We see the following:
```
# Use root/example as user/password credentials
version: '3.1'

services:

  mongo:
    image: mongo
    restart: always
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: example
```
#### But how do we pass these environment variables to mongo applications?
That's easy, there is an _env_ attribute for that in the "container" key, which accepts a list of enviroment variables with names and values. You can hard code the values but that is bad practice. In our case we will reference from secret.


Here is a snippet of the file:

```
containers:
      - name: mongo
        image: mongo:5.0
        ports:
        - containerPort: 27017
        env:
        - name: MONGO_INITDB_ROOT_USERNAME
          valueFrom:
            secretKeyRef:
                name: mongo-secret
                key:  MONGODB_USER
        - name: MONGO_INITDB_ROOT_PASSWORD
          valueFrom:
            secretKeyRef:
                name: mongo-secret
                key: MONGODB_PASSWORD
```             
![image info](referencing secrets.png)

The referencing is done by using the _valueFrom_ properties and _secretKeyRef_. You can give it any name, and the key will be the key of the value you want to access from secrets.
Great, now when the mogodb application starts, a root user with those credentials will be created.

### Pass Config Data to WebApp and Deployment
When the web application starts, it will need to connect to the database, so we need to pass it information, and give it a database endpoint:

Webapp needs information about:
- database endpoint  --> reference from ConfigMap
- database username --> reference from Secret
- database password --> reference from Secret

For this we just copy the environment data we set up in mongo deployment, and paste it the web app deployemnt.
(the application is expecting those environment variables.)
That way the app has the right credentials to access the database.

Next, we pass it the Database endpoint from the configmap. (using the configMapKeyRef), so it knows where to reach the databse

```
- name: DB_URL
  valueFrom:
    configMapKeyRef:  
        name:mongo-config
        key:  mongo-url

```

Finally, we need to make the web app service an external service as it is internal by default.
For this we will add the "type" key to the "spec".
Type has by default the value of _ClusterIP_ which makes it an internal service.
We will set it to "NodePort" to expose the port.
This means that in the "ports" section we will add another key called "nodePort". This is a port that will open on Kubernetes nodes that will make the application accessible.
It exposes the Service on each Node's IP at a static port.

    IMPORTANT!!
_NodePorts in Kubernetes must be between 30000 and 32767_

And this completes the configuration!

### Starting the application:
some quick commands to start and test an application in minikube:
```minikube start --driver docker```
- ```minikibe status ``` will give us a status of the running nodes

- get pod information ```kubectl get pods```

- view the status of nodes and the external ip (the non cluster ip):
```kubectl get nodes -o wide``:

- get services running ``kubectl get svc

- port forward  a service so that it is can be seen in github codespaces: ```kubcetl port-forward svc/<name of service> <port>```


### Push  an image to the github container registry:
1. build an image and tag it with ``` docker build -t ghcr.io/<your github username>/<name of image>:<version> .```
2. In github, create a personal access token and store it somewhere. It must be scoped to read, write and delete packages
3. on the command line log into the container registry with docker, and specify "ghcr.io" at the end so that docker knows to log into ghcr.io rather than defaulting to docker.io
    ```docker login --username=<your github username> --password=< your personal access token> ghcr.io```
4. Once logged in and authenticated push the image to the registry:
    ```docker push ghcr.io/<your github username>/<name of image>:<version>_  ```
    
    
### pull an private image from docker or another registry and run it in Minikube:

1. start minikube ```minikube start --driver docker```
2. ssh into it (we need to be able to give it the container registry credentials and for that we will log into the registry from within minikube)  ```minikube ssh```
3. within minikube log inot the container registry (in this example it is the github container registry):   ```docker login --username=<your github username> --password=< your personal access token> ghcr.io```
4. Once logged in, verify that a file called "config.json" has been created within minikube in the ".docker" directory. This file should contian your credentials to authenticate into the registry: ```cat .docker/config.json```
5. Back into the your host computer, secure copy the config.json file from minikube and replace it with the config.json file located in the host's .docker directory:
```scp -i $(minikube ssh-key) docker@$(minikube ip):.docker/config.json .docker/config.json```
6. verify that the file has indeed been replaced in your host computer:  ```cat .docker/config.json```
7. Encode the file contents to base64 and output the results in the terminal: ```cat .docker/config.json | base64```
8. Create a .Yaml file of type "secret" for kubernetes that looks like this:
```
apiVersion: v1
kind: Secret
metadata:
  name: frontend-registry-key
data:
    # some random b64 data that represents what is in .docker/config.json
    .dockerconfigjson: ewoJImF1dGhzIsdjergergogewoJCSJnaGNyLmlvIjogewoJCQkiYXV0aCI6ICJRbVZoZEhKcGVDMUVjbTlwWkMxTWFXSmxjblI1TFVkc2IySmhiRHBuYUhCZk5GaDRjazlEUldocU1sRmxjSGw2TmpKUmVYVmFkWFJCVTNSaWRGcEpNbkp0UTJKMyIKCQl9Cgl9Cn0=
type: kubernetes.io/dockerconfigjson
```

note the keys in the _data_ field, which MUST BE  _.dockerconfigjson_ and the _type_ which MUST be _kubernetes.io/dockerconfigjson_.
9. Replace the sample b64 encoded string in this file with the base64 encoded content outputted from the terminal. This string is the value of the key _.dockerconfigjson_  in the secret.yaml file.

10. In the  deployment configuration file, reference this secret with the _imagePullSecrets_ attribute under _spec_. The name of the imagePullSecret must match the name in the metadata of the secret.yaml.  This secret will provide the authentication credentials for when Kubernetes tries to pull down a private image 

```apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend-deployment
  labels:
    app: frontend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
    # this is a special attribute for pulling private images
      imagePullSecrets:
      - name: frontend-registry-key
      containers:
      - name: frontend
        image: ghcr.io/beatrix-droid-liberty-global/recon-ui:latest  
        ports:
        - containerPort: 80
  ```
