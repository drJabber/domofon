-- name: get-client-by-client_id^
SELECT id,
       client_id,
       salt,
       hashed_secret,
       created_at,
       updated_at
FROM clients
WHERE client_id = :client_id
LIMIT 1;


-- name: create-new-client<!
INSERT INTO clients (client_id, salt, hashed_secret)
VALUES (:client_id, :salt, :hashed_secret)
RETURNING
    id, created_at, updated_at;


-- name: update-client-by-client_id<!
UPDATE
    clients
SET client_id        = :new_client_id,
    salt            = :new_salt,
    hashed_secret = :new_secret
WHERE client_id = :client_id
RETURNING
    updated_at;
