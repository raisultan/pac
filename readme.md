# PAC

### Constraints
1. Ticket Body Max Characters: 500 characters.

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

4. Categorizer: given a ticket categorizes it to be one of available categories.

5. Event Composer: composes BI event from original ticket and any data outputed or used during processing

6. Data Lake Repository: sends data to data lake.
