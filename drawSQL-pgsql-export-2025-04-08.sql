CREATE TABLE "users"(
    "id" UUID NOT NULL,
    "email" VARCHAR(255) NOT NULL,
    "hashed_password" VARCHAR(255) NOT NULL,
    "first_name" TEXT NOT NULL,
    "middle_name" TEXT NULL,
    "last_name" TEXT NOT NULL,
    "description" TEXT NULL,
    "phone_number" TEXT NOT NULL,
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL
);
ALTER TABLE
    "users" ADD PRIMARY KEY("id");
ALTER TABLE
    "users" ADD CONSTRAINT "users_email_unique" UNIQUE("email");
ALTER TABLE
    "users" ADD CONSTRAINT "users_phone_number_unique" UNIQUE("phone_number");
CREATE TABLE "students"(
    "id" UUID NOT NULL,
    "user_id" UUID NOT NULL,
    "level" UUID NOT NULL,
    "terminated" BOOLEAN NOT NULL DEFAULT '0'
);
ALTER TABLE
    "students" ADD PRIMARY KEY("id");
CREATE TABLE "levels"(
    "id" UUID NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT NULL,
    "terminated" BOOLEAN NOT NULL
);
ALTER TABLE
    "levels" ADD PRIMARY KEY("id");
CREATE TABLE "teachers"(
    "id" UUID NOT NULL,
    "user_id" UUID NOT NULL,
    "terminated" BOOLEAN NOT NULL DEFAULT '0'
);
ALTER TABLE
    "teachers" ADD PRIMARY KEY("id");
CREATE TABLE "admins"(
    "id" UUID NOT NULL,
    "user_id" UUID NOT NULL
);
ALTER TABLE
    "admins" ADD PRIMARY KEY("id");
CREATE TABLE "slots"(
    "id" UUID NOT NULL,
    "teacher_id" UUID NOT NULL,
    "day_of_week" INTEGER NOT NULL,
    "time" TIME(0) WITHOUT TIME ZONE NOT NULL
);
ALTER TABLE
    "slots" ADD PRIMARY KEY("id");
CREATE TABLE "teacher_lessons"(
    "teacher_id" UUID NOT NULL,
    "lesson_id" UUID NOT NULL
);
ALTER TABLE
    "teacher_lessons" ADD PRIMARY KEY("teacher_id");
ALTER TABLE
    "teacher_lessons" ADD PRIMARY KEY("lesson_id");
CREATE TABLE "lessons"(
    "id" UUID NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT NULL,
    "lesson_type" UUID NOT NULL,
    "start_time" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "finish_time" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "classroom_id" UUID NOT NULL,
    "group_id" UUID NOT NULL,
    "terminated" BOOLEAN NOT NULL DEFAULT '0',
    "is_confirmed" BOOLEAN NOT NULL DEFAULT '0',
    "are_neighbour_allowed" BOOLEAN NOT NULL DEFAULT '0'
);
ALTER TABLE
    "lessons" ADD PRIMARY KEY("id");
CREATE TABLE "student_groups"(
    "id" UUID NOT NULL,
    "student_id" UUID NOT NULL,
    "group_id" UUID NOT NULL,
    "join_date" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL
);
ALTER TABLE
    "student_groups" ADD PRIMARY KEY("id");
CREATE TABLE "groups"(
    "id" UUID NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT NULL,
    "level" UUID NOT NULL,
    "max_capacity" INTEGER NOT NULL,
    "terminated" BOOLEAN NOT NULL DEFAULT '0'
);
ALTER TABLE
    "groups" ADD PRIMARY KEY("id");
CREATE TABLE "teacher_groups"(
    "teacher_id" UUID NOT NULL,
    "group_id" UUID NOT NULL
);
ALTER TABLE
    "teacher_groups" ADD PRIMARY KEY("teacher_id");
ALTER TABLE
    "teacher_groups" ADD PRIMARY KEY("group_id");
CREATE TABLE "events"(
    "id" UUID NOT NULL,
    "evet_type" UUID NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT NULL,
    "start_time" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "photo_url" TEXT NOT NULL,
    "new_column" BIGINT NOT NULL
);
ALTER TABLE
    "events" ADD PRIMARY KEY("id");
CREATE TABLE "event_types"(
    "id" UUID NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT NULL,
    "terminated" BOOLEAN NOT NULL DEFAULT '0'
);
ALTER TABLE
    "event_types" ADD PRIMARY KEY("id");
CREATE TABLE "subscriptions"(
    "id" UUID NOT NULL,
    "student_id" UUID NOT NULL,
    "subscription_template_id" UUID NULL,
    "expiration_date" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "payment_id" UUID NULL
);
ALTER TABLE
    "subscriptions" ADD PRIMARY KEY("id");
CREATE TABLE "subscription_template"(
    "id" UUID NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT NULL,
    "lesson_count" INTEGER NOT NULL,
    "expiration_date" TIMESTAMP(0) WITHOUT TIME ZONE NULL,
    "expiration_day_count" INTEGER NULL,
    "price" DECIMAL(8, 2) NOT NULL,
    "active" BOOLEAN NOT NULL
);
ALTER TABLE
    "subscription_template" ADD PRIMARY KEY("id");
ALTER TABLE
    "admins" ADD CONSTRAINT "admins_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "users"("id");
ALTER TABLE
    "events" ADD CONSTRAINT "events_evet_type_foreign" FOREIGN KEY("evet_type") REFERENCES "event_types"("id");
ALTER TABLE
    "subscriptions" ADD CONSTRAINT "subscriptions_subscription_template_id_foreign" FOREIGN KEY("subscription_template_id") REFERENCES "subscription_template"("id");
ALTER TABLE
    "teachers" ADD CONSTRAINT "teachers_id_foreign" FOREIGN KEY("id") REFERENCES "teacher_lessons"("teacher_id");
ALTER TABLE
    "student_groups" ADD CONSTRAINT "student_groups_group_id_foreign" FOREIGN KEY("group_id") REFERENCES "groups"("id");
ALTER TABLE
    "lessons" ADD CONSTRAINT "lessons_group_id_foreign" FOREIGN KEY("group_id") REFERENCES "groups"("id");
ALTER TABLE
    "students" ADD CONSTRAINT "students_level_foreign" FOREIGN KEY("level") REFERENCES "levels"("id");
ALTER TABLE
    "groups" ADD CONSTRAINT "groups_level_foreign" FOREIGN KEY("level") REFERENCES "levels"("id");
ALTER TABLE
    "slots" ADD CONSTRAINT "slots_teacher_id_foreign" FOREIGN KEY("teacher_id") REFERENCES "teachers"("id");
ALTER TABLE
    "student_groups" ADD CONSTRAINT "student_groups_student_id_foreign" FOREIGN KEY("student_id") REFERENCES "students"("id");
ALTER TABLE
    "teacher_groups" ADD CONSTRAINT "teacher_groups_teacher_id_foreign" FOREIGN KEY("teacher_id") REFERENCES "teachers"("id");
ALTER TABLE
    "teachers" ADD CONSTRAINT "teachers_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "users"("id");
ALTER TABLE
    "lessons" ADD CONSTRAINT "lessons_id_foreign" FOREIGN KEY("id") REFERENCES "teacher_lessons"("lesson_id");
ALTER TABLE
    "students" ADD CONSTRAINT "students_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "users"("id");
ALTER TABLE
    "groups" ADD CONSTRAINT "groups_id_foreign" FOREIGN KEY("id") REFERENCES "teacher_groups"("group_id");