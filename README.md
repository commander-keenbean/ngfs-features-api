# ngfs-features-api
This project contains everything you need to spin up an OGC Features API Server from NGFS data

## Prerequisites
1. A kubernetes cluster
2. Helm
3. pipenv (and pyenv is recommended)

## Getting started

1. Install the helm repo bitnami, which provides the postgres chart 

    ```bash
    helm repo add bitnami https://charts.bitnami.com/bitnami
    ```

2. Deploy the postgres chart 

    ```bash
    helm install ngfs-db -f helm/postgres/values.yaml bitnami/postgresql
    ```

3. Get the postgres user password
    ```bash
    export POSTGRES_PASSWORD=$(kubectl get secret --namespace default ngfs-postgres-postgresql -o jsonpath="{.data.postgres-password}" | base64 -d)
    ```

4. Forward postgres port to localhost
    ```bash
    kubectl port-forward --namespace default svc/ngfs-db-postgresql 5432:5432 &
    ```

5. Run the SQL to create the NGFS point store
    ```bash
    PGPASSWORD="$POSTGRES_PASSWORD" psql --host 127.0.0.1 -U postgres -d postgres -p 5432 -a -f sql/NGFS_DETECTIONS.sql
    ```

6. Update the pygeoapi configmap by replacing POSTGREST_PASSWORD in kubernetes/pygeoapi_deployment.yml
    
    On Linux - 
    ```bash
    sed -i "s/POSTGRES_PASSWORD/$(POSTGRES_PASSWORD)/g" kubernetes/pygeoapi_deployment.yml
    ```
    
    On mac
    ```
    sed -i ''  "s/POSTGRES_PASSWORD/${POSTGRES_PASSWORD}/g" kubernetes/pygeoapi_deployment.yml
    ```

7. (Optional) Update the pygeoapi config (starts on line 61 of kubernetes/pygeoapi_deployment.yml)
   
8. Deploy pygeoapi
   ```bash
   kubectl apply -f kubernetes/pygeoapi_deployment.yml
   ```

9. Expose the pygeoapi server on localhost
    ```bash
    kubectl port-forward svc/pygeoapi-server 5000 &
    ```

10. In your browser, navigate to localhost:5000


11. Expose the pygeoapi server on localhost
    ```bash
    kubectl port-forward svc/ngfs-postgres-postgresql 5432 &
    ```


12. Load the data
    ```bash
    cd python/load_ngfs && pipenv sync && pipenv run python load_daily_ngfs_csv.py
    ```


TODO: 
- create kubernetes job to create postgres database
- create kubernetes job to run ngfs load script
- update load script so it doesnt download the file
  