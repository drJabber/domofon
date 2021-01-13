-- name: get-door-by-door_id^
SELECT id,
       door_id,
       ext_door_id,
       ext_user,
       ext_password,
       access_token,
       refresh_token,
       access_token_expires,
       created_at,
       updated_at
FROM doors
WHERE door_id = :door_id
LIMIT 1;

-- name: get-door-by-ext_door_id^
SELECT id,
       door_id,
       ext_door_id,
       ext_user,
       ext_password,
       access_token,
       refresh_token,
       access_token_expires,
       created_at,
       updated_at
FROM doors
WHERE ext_door_id = :ext_door_id
LIMIT 1;


-- name: create-new-door<!
INSERT INTO doors (door_id, ext_door_id, ext_user, ext_password, access_token, refresh_token, access_token_expires)
VALUES (:door_id, :ext_door_id, :ext_user, :ext_password, :access_token, :refresh_token, :access_token_expires)
RETURNING
    id, created_at, updated_at;


-- name: update-door-by-door_id<!
UPDATE
    doors
SET door_id        = :new_door_id,
    ext_door_id    = :new_ext_door_id,
    ext_user       = :new_ext_user,
    ext_password   = :new_ext_password,
    access_token   = :new_access_token,
    refresh_token  = :new_refresh_token,
    access_token_expires = :new_access_token_expires
WHERE door_id = :door_id
RETURNING
    updated_at;
