CREATE TABLE IF NOT EXISTS tasks (
    id TEXT PRIMARY KEY,
    content TEXT NOT NULL,
    description TEXT,
    is_completed BOOLEAN DEFAULT FALSE,
    labels TEXT,  -- JSON array as text
    docid TEXT,
    due_date DATE,
    comments TEXT,
    task_order INTEGER
);

INSERT INTO tasks (id, content, description, is_completed, labels, docid, due_date, comments, task_order) VALUES
('8740816612', 'Return the completed bowel cancer screening test kit', 'This is a letter from the Eastern Programme Hub, Nottingham University Hospitals NHS Trust, reminding Mr. Russell Batchelor to return a completed bowel cancer screening test kit. The letter explains the purpose of the test, provides instructions for obtaining a replacement kit or assistance, and outlines the next steps if the kit is not returned. Action is required to either return the completed test kit or contact the sender for further assistance or to opt out of the screening programme.', FALSE, '["Newsletter"]', '8740816612', '2025-01-07', NULL, 41),
('8752500487', 'Sort landrover car', 'Sort landrover, fix and repair the tranfer box. Send Car to bridge street', FALSE, '[]', '8752500487', '2025-02-01', NULL, 44),
('8752506501', 'Study room sort', NULL, FALSE, '[]', '8752506501', '2025-02-01', 'Study sort\nThrow away unnessary paper and rubbish burn\nEmpty file cabinet\nClear desk\nFile and store anything useful\n<add task details here>\n\nSent from Outlook for iOS<https://aka.ms/o0ukef>\nStudy sort\nThrow away unnessary paper and rubbish burn\nEmpty file cabinet\nClear desk\nFile and store anything useful\n<add task details here>\n\nSent from Outlook for iOS<https://aka.ms/o0ukef>', 45); 