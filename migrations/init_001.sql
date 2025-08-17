BEGIN;

CREATE TABLE alembic_version (
    version_num VARCHAR(32) NOT NULL, 
    CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num)
);

-- Running upgrade  -> 92d9829ade66

CREATE TABLE cities (
    id BIGSERIAL NOT NULL, 
    uz VARCHAR(100) NOT NULL, 
    ru VARCHAR(100) NOT NULL, 
    en VARCHAR(100) NOT NULL, 
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), 
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), 
    PRIMARY KEY (id)
);

CREATE TABLE ethnicities (
    id BIGSERIAL NOT NULL, 
    uz_male VARCHAR(100) NOT NULL, 
    uz_female VARCHAR(100) NOT NULL, 
    ru_male VARCHAR(100) NOT NULL, 
    ru_female VARCHAR(100) NOT NULL, 
    en_male VARCHAR(100) NOT NULL, 
    en_female VARCHAR(100) NOT NULL, 
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), 
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), 
    PRIMARY KEY (id)
);

CREATE TABLE marital_statuses (
    id BIGSERIAL NOT NULL, 
    uz_male VARCHAR(100) NOT NULL, 
    uz_female VARCHAR(100) NOT NULL, 
    ru_male VARCHAR(100) NOT NULL, 
    ru_female VARCHAR(100) NOT NULL, 
    en_male VARCHAR(100) NOT NULL, 
    en_female VARCHAR(100) NOT NULL, 
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), 
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), 
    PRIMARY KEY (id)
);

CREATE TABLE religions (
    id BIGSERIAL NOT NULL, 
    uz VARCHAR(100) NOT NULL, 
    ru VARCHAR(100) NOT NULL, 
    en VARCHAR(100) NOT NULL, 
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), 
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), 
    PRIMARY KEY (id)
);

CREATE TABLE users (
    id BIGSERIAL NOT NULL, 
    username VARCHAR(70), 
    language VARCHAR(10) DEFAULT 'en' NOT NULL, 
    status INTEGER DEFAULT '1' NOT NULL, 
    accepted_offer BOOLEAN DEFAULT 'false' NOT NULL, 
    balance_chances INTEGER DEFAULT '0' NOT NULL, 
    last_active_date DATE, 
    daily_streak INTEGER DEFAULT '0' NOT NULL, 
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), 
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), 
    PRIMARY KEY (id)
);

CREATE TYPE entrykind AS ENUM ('TOP_UP', 'BONUS', 'USAGE', 'ADJUST');

CREATE TYPE source AS ENUM ('Click', 'Payme', 'Uzum', 'Initial', 'Internal');

CREATE TABLE balance_entries (
    id SERIAL NOT NULL, 
    user_id BIGINT NOT NULL, 
    kind entrykind NOT NULL, 
    source source NOT NULL, 
    delta_chances INTEGER NOT NULL, 
    amount_sum INTEGER NOT NULL, 
    payload VARCHAR(100), 
    target_id VARCHAR(100), 
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), 
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), 
    PRIMARY KEY (id), 
    FOREIGN KEY(user_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE TABLE filters (
    id BIGINT NOT NULL, 
    city_id BIGINT, 
    age_from INTEGER, 
    age_to INTEGER, 
    height_from INTEGER, 
    height_to INTEGER, 
    weight_from INTEGER, 
    weight_to INTEGER, 
    goal VARCHAR(50), 
    ethnicity_id BIGINT, 
    has_children BOOLEAN, 
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), 
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), 
    PRIMARY KEY (id), 
    FOREIGN KEY(city_id) REFERENCES cities (id), 
    FOREIGN KEY(ethnicity_id) REFERENCES ethnicities (id), 
    FOREIGN KEY(id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE TABLE matchs (
    id SERIAL NOT NULL, 
    sender_id BIGINT NOT NULL, 
    receiver_id BIGINT NOT NULL, 
    message VARCHAR, 
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), 
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), 
    PRIMARY KEY (id), 
    FOREIGN KEY(receiver_id) REFERENCES users (id), 
    FOREIGN KEY(sender_id) REFERENCES users (id)
);

CREATE TABLE profiles (
    id BIGINT NOT NULL, 
    name VARCHAR(200) NOT NULL, 
    age INTEGER NOT NULL, 
    gender VARCHAR(20) NOT NULL, 
    city_id BIGINT NOT NULL, 
    height INTEGER NOT NULL, 
    weight INTEGER NOT NULL, 
    marital_status_id BIGINT NOT NULL, 
    has_children BOOLEAN NOT NULL, 
    education VARCHAR(50) NOT NULL, 
    goal VARCHAR(50) NOT NULL, 
    religion_id BIGINT NOT NULL, 
    religious_level VARCHAR(20), 
    ethnicity_id BIGINT NOT NULL, 
    job VARCHAR(100), 
    about VARCHAR(300), 
    looking_for VARCHAR(300), 
    is_active BOOLEAN NOT NULL, 
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), 
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), 
    PRIMARY KEY (id), 
    FOREIGN KEY(city_id) REFERENCES cities (id), 
    FOREIGN KEY(ethnicity_id) REFERENCES ethnicities (id), 
    FOREIGN KEY(id) REFERENCES users (id) ON DELETE CASCADE, 
    FOREIGN KEY(marital_status_id) REFERENCES marital_statuses (id), 
    FOREIGN KEY(religion_id) REFERENCES religions (id)
);

CREATE TABLE viewed_profiles (
    id SERIAL NOT NULL, 
    viewer_id BIGINT NOT NULL, 
    viewed_user_id BIGINT NOT NULL, 
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), 
    updated_at TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), 
    PRIMARY KEY (id), 
    FOREIGN KEY(viewed_user_id) REFERENCES users (id) ON DELETE CASCADE, 
    FOREIGN KEY(viewer_id) REFERENCES users (id) ON DELETE CASCADE, 
    CONSTRAINT uq_viewed_profiles UNIQUE (viewer_id, viewed_user_id)
);

INSERT INTO alembic_version (version_num) VALUES ('92d9829ade66') RETURNING alembic_version.version_num;

COMMIT;

