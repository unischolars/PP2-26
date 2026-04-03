CREATE OR REPLACE PROCEDURE upsert_contact(p_name VARCHAR, p_phone VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM phonebook WHERE first_name = p_name) THEN
        UPDATE phonebook SET phone = p_phone WHERE first_name = p_name;
    ELSE
        INSERT INTO phonebook(first_name, phone) VALUES(p_name, p_phone);
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE insert_many_contacts(
    p_names VARCHAR[],
    p_phones VARCHAR[]
)
LANGUAGE plpgsql AS $$
DECLARE
    i INT;
    bad_data TEXT := '';
BEGIN
    FOR i IN 1..array_length(p_names, 1) LOOP
        IF p_phones[i] !~ '^\+[0-9]{10,}$' THEN
            bad_data := bad_data || 'Invalid: ' || p_names[i] || ' - ' || p_phones[i] || E'\n';
        ELSE
            INSERT INTO phonebook(first_name, phone)
            VALUES(p_names[i], p_phones[i])
            ON CONFLICT (phone) DO NOTHING;
        END IF;
    END LOOP;

    IF bad_data != '' THEN
        RAISE NOTICE 'Incorrect data:%', bad_data;
    END IF;
END;
$$;

CREATE OR REPLACE PROCEDURE delete_contact(p_value VARCHAR)
LANGUAGE plpgsql AS $$
BEGIN
    DELETE FROM phonebook
    WHERE first_name = p_value OR phone = p_value;
END;
$$;