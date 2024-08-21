import snowflake.connector

# Establish a connection to Snowflake
conn = snowflake.connector.connect(
    user='KRISHNA_EXP',
    password='HDoD5RwjFovGTqd',
    account='streamline.east-us-2.azure',
    warehouse='COMPUTE_WH',
    database='JAMF_MERAKI_WATCHTOWER_DEV_DB',
    schema='RAW_SOURCE_DATA'
)

try:
    # Create a cursor object
    cursor = conn.cursor()

    # Define the query to retrieve key-value pairs from the table
    query = "Select TYPE as key,LANG_CODE as value FROM DEVICE_TYPES WHERE SNAPSHOT_TIME=(Select MAX(SNAPSHOT_TIME) FROM DEVICE_TYPES) GROUP BY TYPE,LANG_CODE"

    # Execute the query
    cursor.execute(query)

    # Fetch all the results
    results = cursor.fetchall()

    # Create a dictionary to map keys to values
    key_value_dict = {row[0]: row[1] for row in results}

    # Print the dictionary
    print(key_value_dict)

finally:
    # Close the cursor and connection
    cursor.close()
    conn.close()
