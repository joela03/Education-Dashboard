CREATE TABLE "enrolment_status" (
    "enrolment_id" BIGINT NOT NULL PRIMARY KEY,
    "enrolment_status" VARCHAR(255) NOT NULL
);

CREATE TABLE "delivery" (
    "delivery_id" BIGINT NOT NULL PRIMARY KEY,
    "delivery_type" VARCHAR(255) NOT NULL
);

CREATE TABLE "student_information" (
    "student_id" BIGINT NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    "name" VARCHAR(255) NOT NULL,
    "mathnasium_id" BIGINT UNIQUE NOT NULL,
    "student_link" VARCHAR(500),
    "enrolment_id" BIGINT,
    "year" BIGINT NOT NULL,
    FOREIGN KEY ("enrolment_id") REFERENCES "enrolment_status"("enrolment_id") ON DELETE SET NULL
);

CREATE TABLE "accounts" (
    "account_id" BIGINT NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    "account_name" VARCHAR(255) NOT NULL UNIQUE,
    "account_link" VARCHAR(500)
);

CREATE TABLE "student_accounts" (
    "student_id" BIGINT NOT NULL,
    "account_id" BIGINT NOT NULL,
    PRIMARY KEY ("student_id", "account_id"),
    FOREIGN KEY ("student_id") REFERENCES "student_information"("student_id") ON DELETE CASCADE,
    FOREIGN KEY ("account_id") REFERENCES "accounts"("account_id") ON DELETE RESTRICT
);

CREATE TABLE "student_education_stats" (
    "student_id" BIGINT NOT NULL UNIQUE PRIMARY KEY,
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
    FOREIGN KEY ("student_id") REFERENCES "student_information"("student_id") ON DELETE CASCADE,
    FOREIGN KEY ("delivery_id") REFERENCES "delivery"("delivery_id") ON DELETE SET NULL
);

CREATE TABLE "guardians" (
    "guardian_id" BIGINT NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    "guardian_name" VARCHAR(255) NOT NULL,
    "guardian_phone" VARCHAR(255)
);

CREATE TABLE "student_guardians" (
    "student_id" BIGINT NOT NULL,
    "guardian_id" BIGINT NOT NULL,
    PRIMARY KEY ("student_id", "guardian_id"),
    FOREIGN KEY ("student_id") REFERENCES "student_information"("student_id") ON DELETE CASCADE,
    FOREIGN KEY ("guardian_id") REFERENCES "guardians"("guardian_id") ON DELETE RESTRICT
);

CREATE TABLE "users" (
    "id" BIGINT NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    "username" VARCHAR(50) NOT NULL UNIQUE,
    "password_hash" VARCHAR(255) NOT NULL,
    "salt" VARCHAR(255) NOT NULL
);

INSERT INTO enrolment_status (enrolment_id, enrolment_status) VALUES 
    (0, 'Enrolment'),
    (1, 'On Hold');

INSERT INTO delivery (delivery_id, delivery_type) VALUES 
    (0, 'In-Centre'),
    (1, '@home');
