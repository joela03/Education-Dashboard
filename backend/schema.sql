CREATE TABLE "students"(
    "id" BIGINT NOT NULL,
    "name" VARCHAR(255) NOT NULL,
    "student_link" VARCHAR(500),
    "enrolment_status" VARCHAR(255) NOT NULL,
    "year" BIGINT NOT NULL,
    "account_name" VARCHAR(255) NOT NULL,
    "account_link" VARCHAR(500),
    "attendance_count" BIGINT NOT NULL,
    "last_attendance" DATE,
    "last_assessment" DATE,
    "active_lps" BIGINT,
    "skills_assigned" BIGINT,
    "skills_mastered" BIGINT,
    "last_lp_update" DATE,
    "last_pr_sent" DATE,
    "last_progress_check" DATE,
    "delivery" VARCHAR(255),
    "virtual_center" VARCHAR(255),
    "mathnasium_id" BIGINT,
    "total_lp_skills_mastered" BIGINT,
    "total_lp_skills" BIGINT,
    "skills_mastered_percent" DECIMAL(5,2),
    PRIMARY KEY("id")
);

CREATE TABLE "guardians"(
    "id" BIGINT NOT NULL GENERATED ALWAYS AS IDENTITY,
    "student_id" BIGINT NOT NULL,
    "guardian_name" VARCHAR(255) NOT NULL,
    "guardian_phone" VARCHAR(255),
    PRIMARY KEY("id"),
    FOREIGN KEY("student_id") REFERENCES "students"("id") ON DELETE CASCADE
);

CREATE TABLE "users"(
    "id" BIGINT NOT NULL GENERATED ALWAYS AS IDENTITY,
    "username" VARCHAR(50) NOT NULL,
    "password_hash" VARCHAR(255) NOT NULL,
    "salt" VARCHAR(255) NOT NULL,
    PRIMARY KEY("id")
);

CREATE TABLE "enrolment_status"(
    "enrolment_id" BIGINT NOT NULL,
    "enrolment_status" VARCHAR(255) NOT NULL,
    PRIMARY KEY("enrolment_id")
);