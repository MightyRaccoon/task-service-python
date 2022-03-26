BEGIN;

CREATE TABLE IF NOT EXISTS tasks (

  task_id SERIAL,
  description TEXT,
  tags TEXT[],
  due_date TIMESTAMP

);

CREATE INDEX IF NOT EXISTS task_id_idx ON tasks (task_id);

COMMIT;