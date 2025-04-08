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
    "terminated" BOOLEAN NOT NULL DEFAULT '0'
);
ALTER TABLE
    "levels" ADD PRIMARY KEY("id");
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
CREATE TABLE "subscriptions"(
    "id" UUID NOT NULL,
    "student_id" UUID NOT NULL,
    "subscription_template_id" UUID NULL,
    "expiration_date" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "payment_id" UUID NULL
);
ALTER TABLE
    "subscriptions" ADD PRIMARY KEY("id");
CREATE TABLE "subscription_templates"(
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
    "subscription_templates" ADD PRIMARY KEY("id");
CREATE TABLE "lesson_subscriptions"(
    "id" UUID NOT NULL,
    "subscription_id" UUID NOT NULL,
    "lesson_id" UUID NOT NULL,
    "cancelled" BOOLEAN NOT NULL DEFAULT '0'
);
ALTER TABLE
    "lesson_subscriptions" ADD PRIMARY KEY("id");
CREATE TABLE "lesson_types"(
    "id" UUID NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT NULL,
    "terminated" BOOLEAN NOT NULL DEFAULT '0'
);
ALTER TABLE
    "lesson_types" ADD PRIMARY KEY("id");
CREATE TABLE "subscription_lesson_types"(
    "subscription_template" UUID NOT NULL,
    "lesson_type_id" UUID NOT NULL
);
ALTER TABLE
    "subscription_lesson_types" ADD PRIMARY KEY("subscription_template");
CREATE TABLE "payments"(
    "id" UUID NOT NULL,
    "time" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "payment_type" UUID NOT NULL,
    "details" TEXT NULL
);
ALTER TABLE
    "payments" ADD PRIMARY KEY("id");
CREATE TABLE "payment_type"(
    "id" UUID NOT NULL,
    "name" TEXT NOT NULL
);
ALTER TABLE
    "payment_type" ADD PRIMARY KEY("id");
CREATE TABLE "classrooms"(
    "id" UUID NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT NULL,
    "terminated" BOOLEAN NOT NULL DEFAULT '0'
);
ALTER TABLE
    "classrooms" ADD PRIMARY KEY("id");
ALTER TABLE
    "subscription_templates" ADD CONSTRAINT "subscription_templates_id_foreign" FOREIGN KEY("id") REFERENCES "subscription_lesson_types"("subscription_template");
ALTER TABLE
    "lesson_subscriptions" ADD CONSTRAINT "lesson_subscriptions_subscription_id_foreign" FOREIGN KEY("subscription_id") REFERENCES "subscriptions"("id");
ALTER TABLE
    "subscriptions" ADD CONSTRAINT "subscriptions_payment_id_foreign" FOREIGN KEY("payment_id") REFERENCES "payments"("id");
ALTER TABLE
    "subscription_lesson_types" ADD CONSTRAINT "subscription_lesson_types_lesson_type_id_foreign" FOREIGN KEY("lesson_type_id") REFERENCES "lesson_types"("id");
ALTER TABLE
    "payments" ADD CONSTRAINT "payments_payment_type_foreign" FOREIGN KEY("payment_type") REFERENCES "payment_type"("id");
ALTER TABLE
    "subscriptions" ADD CONSTRAINT "subscriptions_subscription_template_id_foreign" FOREIGN KEY("subscription_template_id") REFERENCES "subscription_templates"("id");
ALTER TABLE
    "student_groups" ADD CONSTRAINT "student_groups_group_id_foreign" FOREIGN KEY("group_id") REFERENCES "groups"("id");
ALTER TABLE
    "lessons" ADD CONSTRAINT "lessons_group_id_foreign" FOREIGN KEY("group_id") REFERENCES "groups"("id");
ALTER TABLE
    "students" ADD CONSTRAINT "students_level_foreign" FOREIGN KEY("level") REFERENCES "levels"("id");
ALTER TABLE
    "groups" ADD CONSTRAINT "groups_level_foreign" FOREIGN KEY("level") REFERENCES "levels"("id");
ALTER TABLE
    "student_groups" ADD CONSTRAINT "student_groups_student_id_foreign" FOREIGN KEY("student_id") REFERENCES "students"("id");
ALTER TABLE
    "lesson_subscriptions" ADD CONSTRAINT "lesson_subscriptions_lesson_id_foreign" FOREIGN KEY("lesson_id") REFERENCES "lessons"("id");
ALTER TABLE
    "lessons" ADD CONSTRAINT "lessons_classroom_id_foreign" FOREIGN KEY("classroom_id") REFERENCES "classrooms"("id");
ALTER TABLE
    "lessons" ADD CONSTRAINT "lessons_lesson_type_foreign" FOREIGN KEY("lesson_type") REFERENCES "lesson_types"("id");
ALTER TABLE
    "lessons" ADD CONSTRAINT "lessons_id_foreign" FOREIGN KEY("id") REFERENCES "teacher_lessons"("lesson_id");
ALTER TABLE
    "groups" ADD CONSTRAINT "groups_id_foreign" FOREIGN KEY("id") REFERENCES "teacher_groups"("group_id");