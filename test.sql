CREATE TABLE test.bonus (
    bonus_id        SERIAL          NOT NULL,
    name            VARCHAR(250)    NOT NULL,
    description     VARCHAR(250)    NOT NULL,
    code            VARCHAR(30)     NOT NULL,
    sys_created_at  TIMESTAMP       CONSTRAINT d_bonus_sys_created_at DEFAULT (CURRENT_TIMESTAMP(0)::TIMESTAMP WITHOUT TIME ZONE) NULL,
    sys_changed_at  TIMESTAMP       CONSTRAINT d_bonus_sys_changed_at DEFAULT (CURRENT_TIMESTAMP(0)::TIMESTAMP WITHOUT TIME ZONE) NULL,
    sys_created_by  INT             CONSTRAINT d_bonus_sys_created_by DEFAULT ((-1)) NULL,
    sys_changed_by  INT             CONSTRAINT d_bonus_sys_changed_by DEFAULT ((-1)) NULL,
    CONSTRAINT k_person PRIMARY KEY (bonus_id),
    CONSTRAINT k_subtask_task_task_id FOREIGN KEY (task_id) REFERENCES lab.task(task_id),
    CONSTRAINT c_subtask_log_subtask_id_student_id UNIQUE  (subtask_id , student_id),
    CONSTRAINT hk_student_id CHECK (student_id > 1),
    CONSTRAINT c_bonus_code UNIQUE (code)
);
