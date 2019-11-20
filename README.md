# Background
The files provided are created assuming the cluster is running within a network on the 192.168.1.0/24 range and currently has 192.168.1.{50,51,52,53} as the staticly assigned ips

The network fabric for this cluster is Weave since some issues were had with Fabric

## Setting up the cluster
The first thing to do is flash HypriotOS onto the sd card for the raspberry pi which can be done with the command listed below.
I created an individual file for each node for easier replication.  So when flashing the config-name needs to be replaced in the below command to be the correct configuration.  (The only difference between each of the configs is the hostname and the staticly set ip that it uses) We're using HypriotOS version 1.10.0 as opposed to the latest release because the latest release contains a version of Docker not supported by Kubernetes yet.

```bash
flash -u <config-name>.yaml -c ./device-init.yaml https://github.com/hypriot/image-builder-rpi/releases/download/v1.10.0/hypriotos-rpi-v1.10.0.img.zip
```

Once Hypriot has been installed the repository for Kubernetes needs to be added so Kubeadm can be installed.  This can be done with the commands listed below.
```bash
curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | sudo apt-key add - && \
echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list && \
sudo apt-get update -q && \
sudo apt-get install -qy kubeadm
```

Initialization of the master can be done with 
```bash
sudo kubeadm init 
```
this will eventually give you a command to run on the worker nodes that will be something like `kubeadm join --token <secret token that it generates for you>`

I setup the network fabric before running that command on the workers although in theory it should be fine to run either of that command or the following command, that sets the network fabric up, first. 
```bash
kubectl apply -f “https://cloud.weave.works/k8s/net?k8s-version=$(kubectl version | base64 | tr -d ‘\n’)
```

In order to be able to run any `kubectl` commands and actually interact with the cluster you need to copy the configuration into your home directory.  This can be done with the following series of commands on the master node of the cluster from a non root user.
```
mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config
```
At this point there should be a fully working cluster and running `kubectl get nodes` should return you a list of your nodes and their statuses.