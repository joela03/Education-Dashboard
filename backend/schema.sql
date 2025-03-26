CREATE TABLE "enrolment_status" (
    "enrolment_key" BIGINT NOT NULL PRIMARY KEY,
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
    "delivery_id" BIGINT,
    "year" BIGINT NOT NULL,
    FOREIGN KEY ("delivery_id") REFERENCES "delivery"("delivery_id") ON DELETE SET NULL
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

CREATE TABLE "assessments" (
    "assessment_id" BIGINT NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    "date_taken" DATE NOT NULL,
    "assessment_title" VARCHAR (255) NOT NULL,
    "assessment_level" VARCHAR (255) NOT NULL,
    "score" BIGINT NOT NULL
);

CREATE TABLE "enrolments" (
    "enrolment_id" BIGINT NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    "student_id" BIGINT NOT NULL,
    "enrolment_key" BIGINT,
    "membership" VARCHAR(255) NOT NULL,
    "enrolment_start" DATE NOT NULL,
    "enrolment_end" DATE NOT NULL,
    "total_hold_length" VARCHAR(255) NOT NULL,
    FOREIGN KEY ("student_id") REFERENCES "student_information"("student_id") ON DELETE CASCADE
);

CREATE TABLE assessments_students (
    "assessment_id" BIGINT NOT NULL,
    "student_id" BIGINT NOT NULL,
    PRIMARY KEY ("student_id", "assessment_id"),
    FOREIGN KEY ("student_id") REFERENCES "student_information"("student_id") ON DELETE CASCADE,
    FOREIGN KEY ("assessment_id") REFERENCES "assessments"("assessment_id") ON DELETE RESTRICT
);

CREATE TABLE "student_education_stats" (
    "student_id" BIGINT NOT NULL UNIQUE PRIMARY KEY,
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
    FOREIGN KEY ("student_id") REFERENCES "student_information"("student_id") ON DELETE CASCADE
);

CREATE TABLE holds (
    "hold_id" BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    "student_id" BIGINT NOT NULL,
    "hold_start_date" DATE NOT NULL,
    "hold_end_date" DATE NOT NULL,
    "current_hold_length" VARCHAR(255),
    FOREIGN KEY ("student_id") REFERENCES "student_information"("student_id") ON DELETE CASCADE,
    UNIQUE ("student_id", "hold_start_date")
);

CREATE TABLE "guardians" (
    "guardian_id" BIGINT NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
    "guardian_name" VARCHAR(255) NOT NULL UNIQUE,
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

INSERT INTO enrolment_status (enrolment_key, enrolment_status) VALUES 
    (0, 'Enrolment'),
    (1, 'On Hold'),
    (2, 'Pre-Enroled');

INSERT INTO delivery (delivery_id, delivery_type) VALUES 
    (0, 'In-Centre'),
    (1, '@home'),
    (2, 'Hybrid');
