alias k=kubectl
k apply -f ConfigMapAndSecret.yml
k apply -f PersistVolume.yml
k apply -f PersistVolumeClaim.yml
k apply -f Deployment.yml
k apply -f Service.yml