from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "patient" (
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMP,
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "age" INT NOT NULL,
    "gender" VARCHAR(31) NOT NULL,
    "birthday" TIMESTAMP NOT NULL
);
CREATE INDEX IF NOT EXISTS "idx_patient_id_3abb4a" ON "patient" ("id", "name");
CREATE TABLE IF NOT EXISTS "hospital" (
    "created_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "deleted_at" TIMESTAMP,
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "plan_name" VARCHAR(255) NOT NULL,
    "status" VARCHAR(255) NOT NULL,
    "person_id" INT NOT NULL REFERENCES "patient" ("id") ON DELETE CASCADE
) /* Plans: */;
CREATE INDEX IF NOT EXISTS "idx_hospital_person__ceee40" ON "hospital" ("person_id", "status");
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSON NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
