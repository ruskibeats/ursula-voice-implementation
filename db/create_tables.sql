-- Create base tables
CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS task_priority (
    id SERIAL PRIMARY KEY,
    task_id INTEGER REFERENCES tasks(id),
    priority_level TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS recurring_tasks (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    frequency TEXT,
    next_due TIMESTAMP,
    status TEXT DEFAULT 'PENDING',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert some test data
INSERT INTO tasks (title, description, status) VALUES 
('Pay IRS', 'Monthly tax payment', 'PENDING'),
('Doctor Appointment', 'Annual checkup', 'PENDING');

INSERT INTO recurring_tasks (title, frequency, next_due) VALUES 
('Weekly Review', 'WEEKLY', CURRENT_TIMESTAMP + INTERVAL '7 days'),
('Monthly Tax Check', 'MONTHLY', CURRENT_TIMESTAMP + INTERVAL '30 days'); 