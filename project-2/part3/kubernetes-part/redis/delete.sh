alias k=kubectl
k delete -f ConfigMapAndSecret.yml
k delete -f Deployment.yml
k delete -f PersistVolumeClaim.yml
k delete -f PersistVolume.yml
k delete -f Service.yml