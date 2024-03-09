Create "test" topic locally
```
docker exec -it <kafka-id> kafka-topics --create --topic test --partitions 1 --replication-factor 1 --bootstrap-server localhost:9092
```

Send data to topic
```
docker exec -it <kafka-id> kafka-console-producer --broker-list localhost:9092 --topic test
```
