#!/bin/bash
# Scale SQL Database
RESOURCE_GROUP=$1
SERVER_NAME=$2
DB_NAME=$3
NEW_SKU=$4

az sql db update \
    --resource-group $RESOURCE_GROUP \
    --server $SERVER_NAME \
    --name $DB_NAME \
    --service-objective $NEW_SKU
