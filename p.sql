DROP TABLE users;
CREATE TABLE users (
    first_name varchar(40),
    last_name varchar(40),
    name varchar(50),
    registered_user boolean,
    data_sources varchar(100),
    id integer,
    bio varchar(1000),
    skills varchar(100),
    skill_string varchar(100),
    needs varchar(100),
    need_string varchar(100),
    linkedin_token varchar(40),
    github_token varchar(40),
    linkedin_username varchar(40),
    github_username varchar(40),
    linkedin_data_api varchar(1000),
    linkedin_data_scrape varchar(1000),
    linkedin_contact varchar(100),
    github_data varchar(1000),
    photo varchar(100),
    memberships varchar(50),
    jobs varchar(50),
    past_employers varchar(50),
    confirmed_skills varchar(100)
    -- github_data_api varchar(1000),
    -- created_at timestamp,
    -- updated_at timestamp
);
\COPY users from '/home/wangjing/Programming/phhackthon/peoplehuntpy/md2.csv' DELIMITER ',' CSV HEADER; 
