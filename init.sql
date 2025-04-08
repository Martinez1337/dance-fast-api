-- Включение расширения для работы с UUID
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Создание таблицы пользователей
CREATE TABLE "users"(
    "id" UUID NOT NULL DEFAULT uuid_generate_v4(),
    "email" VARCHAR(255) NOT NULL,
    "hashed_password" VARCHAR(255) NOT NULL,
    "first_name" TEXT NOT NULL,
    "middle_name" TEXT NULL,
    "last_name" TEXT NOT NULL,
    "description" TEXT NULL,
    "phone_number" TEXT NOT NULL,
    "created_at" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "users_pkey" PRIMARY KEY("id"),
    CONSTRAINT "users_email_unique" UNIQUE("email"),
    CONSTRAINT "users_phone_number_unique" UNIQUE("phone_number")
);

-- Создание таблицы уровней
CREATE TABLE "levels"(
    "id" UUID NOT NULL DEFAULT uuid_generate_v4(),
    "name" TEXT NOT NULL,
    "description" TEXT NULL,
    "terminated" BOOLEAN NOT NULL DEFAULT false,
    CONSTRAINT "levels_pkey" PRIMARY KEY("id")
);

-- Создание таблицы типов уроков
CREATE TABLE "lesson_types"(
    "id" UUID NOT NULL DEFAULT uuid_generate_v4(),
    "name" TEXT NOT NULL,
    "description" TEXT NULL,
    "terminated" BOOLEAN NOT NULL DEFAULT false,
    CONSTRAINT "lesson_types_pkey" PRIMARY KEY("id")
);

-- Создание таблицы аудиторий
CREATE TABLE "classrooms"(
    "id" UUID NOT NULL DEFAULT uuid_generate_v4(),
    "name" TEXT NOT NULL,
    "description" TEXT NULL,
    "terminated" BOOLEAN NOT NULL DEFAULT false,
    CONSTRAINT "classrooms_pkey" PRIMARY KEY("id")
);

-- Создание таблицы групп
CREATE TABLE "groups"(
    "id" UUID NOT NULL DEFAULT uuid_generate_v4(),
    "name" TEXT NOT NULL,
    "description" TEXT NULL,
    "level" UUID NOT NULL,
    "max_capacity" INTEGER NOT NULL,
    "terminated" BOOLEAN NOT NULL DEFAULT false,
    CONSTRAINT "groups_pkey" PRIMARY KEY("id"),
    CONSTRAINT "groups_level_foreign" FOREIGN KEY("level") REFERENCES "levels"("id")
);

-- Создание таблицы студентов
CREATE TABLE "students"(
    "id" UUID NOT NULL DEFAULT uuid_generate_v4(),
    "user_id" UUID NOT NULL,
    "level" UUID NOT NULL,
    "terminated" BOOLEAN NOT NULL DEFAULT false,
    CONSTRAINT "students_pkey" PRIMARY KEY("id"),
    CONSTRAINT "students_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "users"("id"),
    CONSTRAINT "students_level_foreign" FOREIGN KEY("level") REFERENCES "levels"("id")
);

-- Создание таблицы преподавателей
CREATE TABLE "teachers"(
    "id" UUID NOT NULL DEFAULT uuid_generate_v4(),
    "user_id" UUID NOT NULL,
    "terminated" BOOLEAN NOT NULL DEFAULT false,
    CONSTRAINT "teachers_pkey" PRIMARY KEY("id"),
    CONSTRAINT "teachers_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "users"("id")
);

-- Создание таблицы администраторов
CREATE TABLE "admins"(
    "id" UUID NOT NULL DEFAULT uuid_generate_v4(),
    "user_id" UUID NOT NULL,
    CONSTRAINT "admins_pkey" PRIMARY KEY("id"),
    CONSTRAINT "admins_user_id_foreign" FOREIGN KEY("user_id") REFERENCES "users"("id")
);

-- Создание таблицы слотов преподавателей
CREATE TABLE "slots"(
    "id" UUID NOT NULL DEFAULT uuid_generate_v4(),
    "teacher_id" UUID NOT NULL,
    "day_of_week" INTEGER NOT NULL,
    "time" TIME(0) WITHOUT TIME ZONE NOT NULL,
    CONSTRAINT "slots_pkey" PRIMARY KEY("id"),
    CONSTRAINT "slots_teacher_id_foreign" FOREIGN KEY("teacher_id") REFERENCES "teachers"("id")
);

-- Создание таблицы уроков
CREATE TABLE "lessons"(
    "id" UUID NOT NULL DEFAULT uuid_generate_v4(),
    "name" TEXT NOT NULL,
    "description" TEXT NULL,
    "lesson_type" UUID NOT NULL,
    "start_time" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "finish_time" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "classroom_id" UUID NOT NULL,
    "group_id" UUID NOT NULL,
    "terminated" BOOLEAN NOT NULL DEFAULT false,
    "is_confirmed" BOOLEAN NOT NULL DEFAULT false,
    "are_neighbour_allowed" BOOLEAN NOT NULL DEFAULT false,
    CONSTRAINT "lessons_pkey" PRIMARY KEY("id"),
    CONSTRAINT "lessons_lesson_type_foreign" FOREIGN KEY("lesson_type") REFERENCES "lesson_types"("id"),
    CONSTRAINT "lessons_classroom_id_foreign" FOREIGN KEY("classroom_id") REFERENCES "classrooms"("id"),
    CONSTRAINT "lessons_group_id_foreign" FOREIGN KEY("group_id") REFERENCES "groups"("id")
);

-- Создание таблицы связей преподавателей и уроков
CREATE TABLE "teacher_lessons"(
    "teacher_id" UUID NOT NULL,
    "lesson_id" UUID NOT NULL,
    CONSTRAINT "teacher_lessons_pkey" PRIMARY KEY("teacher_id", "lesson_id"),
    CONSTRAINT "teacher_lessons_teacher_id_foreign" FOREIGN KEY("teacher_id") REFERENCES "teachers"("id"),
    CONSTRAINT "teacher_lessons_lesson_id_foreign" FOREIGN KEY("lesson_id") REFERENCES "lessons"("id")
);

-- Создание таблицы связей студентов и групп
CREATE TABLE "student_groups"(
    "id" UUID NOT NULL DEFAULT uuid_generate_v4(),
    "student_id" UUID NOT NULL,
    "group_id" UUID NOT NULL,
    "join_date" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT "student_groups_pkey" PRIMARY KEY("id"),
    CONSTRAINT "student_groups_student_id_foreign" FOREIGN KEY("student_id") REFERENCES "students"("id"),
    CONSTRAINT "student_groups_group_id_foreign" FOREIGN KEY("group_id") REFERENCES "groups"("id")
);

-- Создание таблицы связей преподавателей и групп
CREATE TABLE "teacher_groups"(
    "teacher_id" UUID NOT NULL,
    "group_id" UUID NOT NULL,
    CONSTRAINT "teacher_groups_pkey" PRIMARY KEY("teacher_id", "group_id"),
    CONSTRAINT "teacher_groups_teacher_id_foreign" FOREIGN KEY("teacher_id") REFERENCES "teachers"("id"),
    CONSTRAINT "teacher_groups_group_id_foreign" FOREIGN KEY("group_id") REFERENCES "groups"("id")
);

-- Создание таблицы типов событий
CREATE TABLE "event_types"(
    "id" UUID NOT NULL DEFAULT uuid_generate_v4(),
    "name" TEXT NOT NULL,
    "description" TEXT NULL,
    "terminated" BOOLEAN NOT NULL DEFAULT false,
    CONSTRAINT "event_types_pkey" PRIMARY KEY("id")
);

-- Создание таблицы событий
CREATE TABLE "events"(
    "id" UUID NOT NULL DEFAULT uuid_generate_v4(),
    "event_type" UUID NOT NULL,
    "name" TEXT NOT NULL,
    "description" TEXT NULL,
    "start_time" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "photo_url" TEXT NOT NULL,
    CONSTRAINT "events_pkey" PRIMARY KEY("id"),
    CONSTRAINT "events_event_type_foreign" FOREIGN KEY("event_type") REFERENCES "event_types"("id")
);

-- Создание таблицы шаблонов подписок
CREATE TABLE "subscription_templates"(
    "id" UUID NOT NULL DEFAULT uuid_generate_v4(),
    "name" TEXT NOT NULL,
    "description" TEXT NULL,
    "lesson_count" INTEGER NOT NULL,
    "expiration_date" TIMESTAMP(0) WITHOUT TIME ZONE NULL,
    "expiration_day_count" INTEGER NULL,
    "price" DECIMAL(8, 2) NOT NULL,
    "active" BOOLEAN NOT NULL DEFAULT true,
    CONSTRAINT "subscription_templates_pkey" PRIMARY KEY("id")
);

-- Создание таблицы типов платежей
CREATE TABLE "payment_types"(
    "id" UUID NOT NULL DEFAULT uuid_generate_v4(),
    "name" TEXT NOT NULL,
    CONSTRAINT "payment_types_pkey" PRIMARY KEY("id")
);

-- Создание таблицы платежей
CREATE TABLE "payments"(
    "id" UUID NOT NULL DEFAULT uuid_generate_v4(),
    "time" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "payment_type" UUID NOT NULL,
    "details" TEXT NULL,
    CONSTRAINT "payments_pkey" PRIMARY KEY("id"),
    CONSTRAINT "payments_payment_type_foreign" FOREIGN KEY("payment_type") REFERENCES "payment_types"("id")
);

-- Создание таблицы подписок
CREATE TABLE "subscriptions"(
    "id" UUID NOT NULL DEFAULT uuid_generate_v4(),
    "student_id" UUID NOT NULL,
    "subscription_template_id" UUID NULL,
    "expiration_date" TIMESTAMP(0) WITHOUT TIME ZONE NOT NULL,
    "payment_id" UUID NULL,
    CONSTRAINT "subscriptions_pkey" PRIMARY KEY("id"),
    CONSTRAINT "subscriptions_student_id_foreign" FOREIGN KEY("student_id") REFERENCES "students"("id"),
    CONSTRAINT "subscriptions_subscription_template_id_foreign" FOREIGN KEY("subscription_template_id") REFERENCES "subscription_templates"("id"),
    CONSTRAINT "subscriptions_payment_id_foreign" FOREIGN KEY("payment_id") REFERENCES "payments"("id")
);

-- Создание таблицы связей подписок и уроков
CREATE TABLE "lesson_subscriptions"(
    "id" UUID NOT NULL DEFAULT uuid_generate_v4(),
    "subscription_id" UUID NOT NULL,
    "lesson_id" UUID NOT NULL,
    "cancelled" BOOLEAN NOT NULL DEFAULT false,
    CONSTRAINT "lesson_subscriptions_pkey" PRIMARY KEY("id"),
    CONSTRAINT "lesson_subscriptions_subscription_id_foreign" FOREIGN KEY("subscription_id") REFERENCES "subscriptions"("id"),
    CONSTRAINT "lesson_subscriptions_lesson_id_foreign" FOREIGN KEY("lesson_id") REFERENCES "lessons"("id")
);

-- Создание таблицы связей шаблонов подписок и типов уроков
CREATE TABLE "subscription_lesson_types"(
    "subscription_template_id" UUID NOT NULL,
    "lesson_type_id" UUID NOT NULL,
    CONSTRAINT "subscription_lesson_types_pkey" PRIMARY KEY("subscription_template_id", "lesson_type_id"),
    CONSTRAINT "subscription_lesson_types_subscription_template_id_foreign" FOREIGN KEY("subscription_template_id") REFERENCES "subscription_templates"("id"),
    CONSTRAINT "subscription_lesson_types_lesson_type_id_foreign" FOREIGN KEY("lesson_type_id") REFERENCES "lesson_types"("id")
);
