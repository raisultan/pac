start-milvus:
	docker compose -f docker/milvus.yaml up -d
stop-milvus:
	docker compose -f docker/milvus.yaml stop

start-kafka:
	docker compose -f docker/kafka.yaml up -d
stop-kafka:
	docker compose -f docker/kafka.yaml stop

run:
	faststream run pac.main:app

create-collection:
	PYTHONPATH=. python3 pac/utils/create_collection.py

# ----------------------------------------------- Testing Utility ------------------------------------------------------

# Dummy target for capturing any argument that doesn't match a target name
%:
	@:

# A function to extract the nth word from the command line
extract_nth_arg = $(word $1, $(MAKECMDGOALS))

CONTAINER_ID := $(call extract_nth_arg,2)

.PHONY: create-input-topic
create-input-topic:
	docker exec -it $(CONTAINER_ID) kafka-topics --create --topic test --partitions 1 --replication-factor 1 --bootstrap-server localhost:9092

.PHONY: write-to-input-topic
write-to-input-topic:
	docker exec -it $(CONTAINER_ID) kafka-console-producer --broker-list localhost:9092 --topic test

.PHONY: monitor-output-topic
monitor-output-topic:
	docker exec -it $(CONTAINER_ID) kafka-console-consumer --topic test_out --from-beginning --bootstrap-server localhost:9092
