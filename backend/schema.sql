CREATE TABLE "enrolment_status" (
    "enrolment_id" BIGINT NOT NULL PRIMARY KEY,
    "enrolment_status" VARCHAR(255) NOT NULL
);

CREATE TABLE "delivery" (
    "delivery_id" BIGINT NOT NULL PRIMARY KEY,
    "delivery_type" VARCHAR(255) NOT NULL
);

CREATE TABLE "student_information" (
    "id" BIGINT NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    "name" VARCHAR(255) NOT NULL,
    "student_link" VARCHAR(500),
    "enrolment_id" BIGINT,
    "year" BIGINT NOT NULL,
    FOREIGN KEY ("enrolment_id") REFERENCES "enrolment_status"("enrolment_id") ON DELETE SET NULL
);

CREATE TABLE "account" (
    "id" BIGINT NOT NULL PRIMARY KEY,
    "student_id" BIGINT NOT NULL UNIQUE,
    "account_name" VARCHAR(255) NOT NULL,
    "account_link" VARCHAR(500),
    FOREIGN KEY ("student_id") REFERENCES "student_information"("id") ON DELETE CASCADE
);

CREATE TABLE "student_education_stats" (
    "id" BIGINT NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    "student_id" BIGINT NOT NULL UNIQUE,
    "delivery_id" BIGINT,
    "attendance_count" BIGINT,
    "last_attendance" DATE,
    "last_assessment" DATE,
    "active_lps" BIGINT,
    "skills_assigned" BIGINT,
    "skills_mastered" BIGINT,
    "last_lp_update" DATE,
    "last_pr_sent" DATE,
    "last_progress_check" DATE,
    "mathnasium_id" BIGINT,
    "total_lp_skills_mastered" BIGINT,
    "total_lp_skills" BIGINT,
    "skills_mastered_percent" DECIMAL(5,2),
    FOREIGN KEY ("student_id") REFERENCES "student_information"("id") ON DELETE CASCADE,
    FOREIGN KEY ("delivery_id") REFERENCES "delivery"("delivery_id") ON DELETE SET NULL
);

CREATE TABLE "guardians" (
    "id" BIGINT NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    "guardian_name" VARCHAR(255) NOT NULL,
    "guardian_phone" VARCHAR(255)
);

CREATE TABLE "student_guardians" (
    "student_id" BIGINT NOT NULL,
    "guardian_id" BIGINT NOT NULL,
    PRIMARY KEY ("student_id", "guardian_id"),
    FOREIGN KEY ("student_id") REFERENCES "student_information"("id") ON DELETE CASCADE,
    FOREIGN KEY ("guardian_id") REFERENCES "guardians"("id") ON DELETE RESTRICT
);

CREATE TABLE "users" (
    "id" BIGINT NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    "username" VARCHAR(50) NOT NULL UNIQUE,
    "password_hash" VARCHAR(255) NOT NULL,
    "salt" VARCHAR(255) NOT NULL
);

INSERT INTO enrolment_status (enrolment_id, enrolment_status) VALUES 
    (0, 'Enrolled'),
    (1, 'On Hold');

INSERT INTO delivery (delivery_id, delivery_type) VALUES 
    (0, 'In-Centre'),
    (1, '@home');
