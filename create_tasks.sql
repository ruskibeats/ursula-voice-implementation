DROP TABLE IF EXISTS public.tasks;

CREATE TABLE public.tasks (
    id TEXT PRIMARY KEY,
    content TEXT NOT NULL,
    description TEXT,
    is_completed BOOLEAN DEFAULT FALSE,
    labels TEXT,  -- JSON array as text
    docid TEXT,
    "Due Date" DATE,
    "Comments" TEXT,
    "Order" INTEGER
); 