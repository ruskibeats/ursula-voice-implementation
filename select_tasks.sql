SELECT 
    t.id,
    t.message_id,
    t.contact_id,
    t.status,
    t.priority,
    t.created_at,
    t.completed_at,
    t.description
FROM public.tasks t
ORDER BY t.created_at DESC; 