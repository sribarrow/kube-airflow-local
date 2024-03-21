1. Install and Setup up Kubernetes cluster
2. Setup K8 dashboard
3. Install helm
4. Install and Run Apache Airflow in K8 pods

# To see airflow UI after install
```
kubectl port-forward svc/airflow-webserver 8080:8080 --namespace airflow
```
Type 127.0.0.1:8080 in your browser and login with admin/admin.

# To see config values
```
helm show values apache-airflow/airflow > values.yaml
```

# To generate the fernetKey
```
echo Fernet Key: $(kubectl get secret --namespace airflow airflow-fernet-key -o jsonpath="{.data.fernet-key}" | base64 --decode)

```
# update values.yaml to Overide config
## clear all output and add the following
```
fernetKey: {TYPE YOUR FERNET KEY HERE}
webserverSecretKey: {TYPE YOUR FERNET KEY HERE}
executor: "KubernetesExecutor"
```
# To apply config, run
```
helm upgrade --install airflow apache-airflow/airflow --namespace airflow --create-namespace -f values.yaml
```
#### Note the output this time.
> Release "airflow" has been upgraded. Happy Helming!
NAME: airflow
LAST DEPLOYED: Thu Mar 21 06:02:04 2024
NAMESPACE: airflow
STATUS: deployed
REVISION: 2

# Link airflow to git repo
```
dags:
  gitSync:
    enabled: true
    repo: https://github.com/sribarrow/kube-airflow-local.git
    branch: main
    rev: HEAD
    depth: 1
    maxFailures: 0
    subPath: "dags"
```
#### apply config