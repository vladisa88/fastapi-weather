-- upgrade --
CREATE TABLE IF NOT EXISTS "users" (
    "id" CHAR(36) NOT NULL  PRIMARY KEY,
    "email" VARCHAR(255) NOT NULL,
    "hashed_password" VARCHAR(255),
    "is_active" INT NOT NULL  DEFAULT 0,
    "confirmation" CHAR(36)
);
CREATE TABLE IF NOT EXISTS "profile" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "first_name" VARCHAR(50),
    "last_name" VARCHAR(50),
    "user_id" CHAR(36) NOT NULL UNIQUE REFERENCES "users" ("id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "city" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "title" VARCHAR(50) NOT NULL UNIQUE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(20) NOT NULL,
    "content" TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS "profile_city" (
    "profile_id" INT NOT NULL REFERENCES "profile" ("id") ON DELETE CASCADE,
    "city_id" INT NOT NULL REFERENCES "city" ("id") ON DELETE CASCADE
);
