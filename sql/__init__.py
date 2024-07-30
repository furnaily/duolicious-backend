Q_UPDATE_VERIFICATION_LEVEL = """
UPDATE
    person
SET
    verification_level_id = CASE
        WHEN EXISTS (
            SELECT
                1
            FROM
                photo
            WHERE
                person_id = person.id
            AND
                verified
        )
        THEN 3

        WHEN EXISTS (
            SELECT
                1
            FROM
                person p
            WHERE
                p.id = person.id
            AND
                p.verified_age
            AND
                p.verified_gender
        )
        THEN 2

        ELSE 1
    END
WHERE
    id = %(person_id)s
"""

Q_UPSERT_LAST = """
INSERT INTO
    last (server, username, seconds, state)
SELECT
    'duolicious.app',
    %(person_uuid)s::text,
    EXTRACT(EPOCH FROM NOW())::BIGINT,
    ''
WHERE
    %(person_uuid)s IS NOT NULL
ON CONFLICT (server, username) DO UPDATE SET
    seconds  = EXCLUDED.seconds
"""
