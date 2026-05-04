CREATE OR REPLACE FUNCTION get_contacts_by_pattern(p text)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY SELECT c.id, c.first_name, c.phone 
                 FROM phonebook c
                 WHERE c.first_name ILIKE '%' || p || '%'
                    OR c.phone ILIKE '%' || p || '%';
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION get_contacts_paginated(page_size INT, page_number INT)
RETURNS TABLE(id INT, name VARCHAR, phone VARCHAR) AS $$
BEGIN
    RETURN QUERY SELECT c.id, c.first_name, c.phone
                 FROM phonebook c
                 ORDER BY c.id
                 LIMIT page_size OFFSET (page_number - 1) * page_size;
END;
$$ LANGUAGE plpgsql;