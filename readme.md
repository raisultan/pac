# PAC

PAC is a tool for Prioritization and Categorization of support tickets. It enables quick and effortless categorization of support tickets for any kind of product. The main goal of a project is to remove manual human labor and automate the process. It reaches the goal using Vector Semantic Search and LLM function calling.

Quick explanation of the logic behind it is as follows: support ticket data is received by PAC using Kafka topic. PAC first vectorizes ticket data and searches similar vectors in Vector DB using COSINE similarity. In the resulting search result list it takes the most similar and checks the distance between what's given and most similar vector from Vector DB, if the distance is greater than some specific threshold, then the received ticket will be assigned the same category and priority. If the search and threshold check failed, then request to LLM is made, which should return category and priority for the ticket. After the ticket is assigned with priority and category it is inserted into Vector DB. The same process is applied for all the other incoming tickets. This approach saves up costs for LLM requests by first checking the Vector DB and if there is no similar enough ticket, only then it makes the request.

PAC also generates a response event with original ticket data and priority and category and sends it to output topic. So that this event can be further sent to data lake or other storage for later BI or other type of analysis.

In case if priority or category of a certain ticket was assigned incorrectly, there is an API so that correct priority or category can be assigned manually. If such case happens, app sends separate correction event to a separate topic, so that it will be taken to account during analysis.

### Process Flow

```mermaid
flowchart TB
    A[Support Ticket] -->|Received via Kafka Topic| B[Text Normalization]
    B --> C[Request to LLM for Vectorization]
    C -->|Vector Embedding| D{Vector DB Search}

    D -->|If match| E[Check Distance]
    E -->|Below Threshold| F[Assign Category & Priority]
    E -->|Above Threshold| G[LLM Function Call for Priority and Category]
    G --> F
    D -->|No match| G
    
    F -->|Insert into Vector DB| H[Vector DB]
    F --> I[Generate Response Event]
    I -->|Send to Output Topic| J[Data Lake / Storage]
    
    K[Manual API Correction] -.->|If needed| F
    K -->|Correction Event| L[Separate Topic for Analysis]

    style A fill:#4f77f6,stroke:#333,stroke-width:2px
    style B fill:#ffcf33,stroke:#333,stroke-width:4px
    style C fill:#7fd3a4,stroke:#333,stroke-width:4px
    style D fill:#4095c6,stroke:#333,stroke-width:2px
    style E fill:#f98b88,stroke:#333,stroke-width:2px
    style F fill:#8bc34a,stroke:#333,stroke-width:2px
    style G fill:#f06292,stroke:#333,stroke-width:2px
    style H fill:#795548,stroke:#333,stroke-width:2px
    style I fill:#64b5f6,stroke:#333,stroke-width:2px
    style J fill:#ba68c8,stroke:#333,stroke-width:2px
    style K fill:#ffeb3b,stroke:#333,stroke-width:2px
    style L fill:#e91e63,stroke:#333,stroke-width:2px
```

### Tech Stack
- Python 3.10
- Milvus
- Kafka and Zookeeper
- Docker
- OpenAI

### Components
1. Text Normalizer
    - Removes Noise: Strips out irrelevant characters.
    - Standardizes: Converts all characters to lowercase to ensure consistency.
    - Anonymizes: Replaces names, email adresses, phone numbers, and any other user-specific data with generic placeholders.
    - Normalizes URLs and Paths: Converts URLs, file paths, or specific codes to generic placeholders or remove them if they are not relevant to the understanding of the ticket.

2. Vectorizer: creates a vector embedding from given text.

3. Vector DB Repository
    - Searches Similar Tickets
    - Inserts into Vector DB
    - Updates Record in Vector DB
    - Removes Record from Vector DB
    - Gets a Record by ID from Vector DB

4. PAC: given a ticket prioritizes and categorizes it to be one of available categories.

5. Updater: corrects already PACed ticket with given priority and category.

### Getting Started

This section provides instructions on how to set up and run the project using `Poetry` as the package manager.

### Prerequisites

Ensure you have Docker and Poetry installed on your system. These tools are required to run the services and the application.

### Setup and Running Services

1. **Start Milvus**
To start the Milvus database, run the following command:
```bash
   make start-milvus
```

2. **Start Kafka**
To start Kafka for message queuing, execute:
```bash
make start-kafka
```

3. **Install Dependencies**
Install the project dependencies using Poetry:
```bash
poetry install
```

4. **Create Vector Database Collection**
Before running the application, ensure to create the vector database collection with:
```bash
make create-collection
```

5. **Run the Application**
Start the FastAPI application with the following command:
```bash
make run
```

#### Testing Utilities

**Create Input Topic**
You can create a Kafka topic for input tickets by running:
```bash
make create-input-topic CONTAINER_ID=<your_kafka_container_id>
```

**Write to Input Topic**
To send a test ticket to the input topic, use:
```bash
make write-to-input-topic CONTAINER_ID=<your_kafka_container_id>
```

Then, input your test ticket JSON data, for example:
```json
{"id": 123, "email": "test@test.com", "text": "peripherals you sent me are not working. i wanna return them today"}
```

**Monitor Processed Tickets**
To monitor processed tickets:
```bash
make monitor-processed-tickets CONTAINER_ID=<your_kafka_container_id>
```

**Monitor Corrected Tickets**
For monitoring corrected tickets:
```bash
make monitor-corrected-tickets CONTAINER_ID=<your_kafka_container_id>
```

#### Stopping Services

To stop the services, use the following commands:

**Stop Kafka:**
```bash
make stop-kafka
```

**Stop Milvus:**
```bash
make stop-milvus
```

#### API Documentation
For detailed API documentation, visit the FastAPI generated API documentation once the application is running on http://127.0.0.1:8000/docs#/
