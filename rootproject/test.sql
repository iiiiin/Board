-- SELECT CURRENT_USER;
-- SELECT CURRENT_DATABASE();

-- SELECT CURRENT_USER();

-- SELECT CURRENT_USER;

SELECT table_name 
FROM information_schema.tables 
WHERE table_schema = 'public' 
ORDER BY table_name;