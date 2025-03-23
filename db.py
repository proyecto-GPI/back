#db.py
import psycopg2
"""
--Instructions to create the user in the database named 'autoveloz'

CREATE USER autoveloz_creator WITH ENCRYPTED PASSWORD 'autovelozGPI';
ALTER DATABASE autoveloz OWNER TO autoveloz_creator;
GRANT ALL PRIVILEGES ON SCHEMA public TO autoveloz_creator;

"""


# new conn to db
conn = psycopg2.connect(host = "localhost", dbname="autoveloz", user="autoveloz_creator", password="autovelozGPI", port=5432)

cur = conn.cursor()


# we define de 2 types of enum
cur.execute("CREATE TYPE status AS ENUM ('pending', 'confirmed', 'cancelled', 'completed')")
cur.execute("CREATE TYPE customer_type AS ENUM ('individual', 'business')")

# we create the needed tables
tables_statement = """
--office
CREATE TABLE IF NOT EXISTS office (
    id SERIAL PRIMARY KEY,
    address VARCHAR(50)
    -- schedule VARCHAR(20) -- Uncomment if needed, add comma above
);

--users
CREATE TABLE IF NOT EXISTS users (
    id VARCHAR(9) PRIMARY KEY,
    name VARCHAR(20),
    email VARCHAR(50),
    password TEXT NOT NULL,
    customer_type customer_type
);


--booking
CREATE TABLE IF NOT EXISTS booking (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(9) NOT NULL,
   --n_plate VARCHAR(15) NOT NULL,
   --budget_id INTEGER NOT NULL,
    pickUp_id INTEGER NOT NULL,
    return_id INTEGER NOT NULL,
    status status NOT NULL,
    credit_card VARCHAR(16) NOT NULL CHECK (LENGTH(credit_card) = 16 AND credit_card ~ '^[0-9]+$'),
    booking_date TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    pickUp_date TIMESTAMP NOT NULL,
    return_date TIMESTAMP NOT NULL,
    price DECIMAL(10,2),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
  --FOREIGN KEY (n_plate) REFERENCES car(id),
  --FOREIGN KEY (budget_id) REFERENCES budget(id),
    FOREIGN KEY (pickUp_id) REFERENCES office(id),
    FOREIGN KEY (return_id) REFERENCES office(id)
);

"""

cur.execute(tables_statement)


# to save the changes
conn.commit()

# closes the cursor and conn
cur.close()
conn.close()
