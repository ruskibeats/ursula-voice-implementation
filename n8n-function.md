# Function Node Before AI Agent

```javascript
// Validate inputs
if (!Array.isArray($items("INPUTA")) || !Array.isArray($items("INPUTB")) || !Array.isArray($items("INPUTC"))) {
    throw new Error("Invalid input format - expected arrays");
}

// Helper functions
function convertExcelDate(excelDate) {
    if (!excelDate) return null;
    const epoch = new Date(Date.UTC(1899, 11, 30));
    const millisecondsPerDay = 24 * 60 * 60 * 1000;
    return new Date(epoch.getTime() + (excelDate * millisecondsPerDay));
}

function formatDate(date) {
    if (!date) return '';
    const d = new Date(date);
    if (isNaN(d.getTime())) return '';
    const day = String(d.getDate()).padStart(2, '0');
    const month = String(d.getMonth() + 1).padStart(2, '0');
    const year = d.getFullYear();
    return `${day}/${month}/${year}`;
}

// Fetch all items from INPUTA, INPUTB, and INPUTC
const inputA = $items("INPUTA").map(item => {
    if (!item || typeof item.json !== 'object') {
        throw new Error("Invalid INPUTA item format");
    }
    return item.json;
});

const inputB = $items("INPUTB").map(item => {
    if (!item || typeof item.json !== 'object') {
        throw new Error("Invalid INPUTB item format");
    }
    return item.json;
});

const inputC = $items("INPUTC").map(item => {
    if (!item || typeof item.json !== 'object') {
        throw new Error("Invalid INPUTC item format");
    }
    return item.json;
});

// Generate random 3-digit IDs for orphan items in INPUTA
const processedA = inputA.map(doc => {
    if (!doc.id) {
        doc.id = 'todoist' + Date.now().toString(36) + Math.floor(Math.random() * 900 + 100);
    }
    return doc;
});

// Create a Set of string IDs from processed Input A for fast lookup
const idsA = new Set(processedA.map(doc => {
    if (typeof doc.id !== 'string' && typeof doc.id !== 'number') {
        throw new Error("Invalid ID format in INPUTA");
    }
    return String(doc.id);
}));

// Create a Map of comments by task ID for quick lookup
const commentsMap = new Map();
inputC.forEach(comment => {
    if (!comment.task_id) {
        throw new Error("Missing task_id in comment");
    }
    const taskId = String(comment.task_id);
    if (!commentsMap.has(taskId)) {
        commentsMap.set(taskId, []);
    }
    if (typeof comment.content === 'string') {
        commentsMap.get(taskId).push(comment.content);
    }
});

// Update Input B based on ID matching
const updatedB = inputB.map(doc => {
    if (!doc.id) {
        throw new Error("Missing ID in INPUTB document");
    }
    
    const docId = String(doc.id);
    
    // Update completion status
    doc.is_completed = !idsA.has(docId);
    
    // Add comments field with matching comments joined by newlines
    doc.comments = commentsMap.has(docId) ? 
        commentsMap.get(docId).join('\n') : 
        '';
        
    // Handle Due Date
    if (!doc["Due Date"]) {
        const postedAt = $item("2").$node["INPUTC"].json["posted_at"];
        if (postedAt) {
            const postedDate = new Date(postedAt);
            const dueDate = new Date(postedDate);
            dueDate.setDate(dueDate.getDate() + 5);
            doc["Due Date"] = formatDate(dueDate);
        }
    } else {
        // Convert existing date if it's a number (Excel/Sheets format)
        if (typeof doc["Due Date"] === 'number') {
            doc["Due Date"] = formatDate(convertExcelDate(doc["Due Date"]));
        } else if (typeof doc["Due Date"] === 'string') {
            // Try to parse and reformat existing date string
            const parsedDate = new Date(doc["Due Date"]);
            if (!isNaN(parsedDate.getTime())) {
                doc["Due Date"] = formatDate(parsedDate);
            } else {
                doc["Due Date"] = '';
            }
        }
    }
        
    return doc;
});

// Get all tasks from updatedB
const tasks = updatedB.map(item => {
    // Pass through all fields from item
    const task = { ...item };
    
    // Ensure critical fields
    task.id = item.id;  // Todoist ID
    task.is_completed = item.is_completed;
    
    return task;
});

// Process and categorize tasks - only process incomplete tasks
const processedTasks = tasks
    .filter(task => task && task.content && task['Due Date'] && !task.is_completed)
    .map(task => {
        // Handle date conversion
        let dueDate = task['Due Date'];
        if (typeof dueDate === 'number') {
            dueDate = formatDate(convertExcelDate(dueDate));
        } else if (typeof dueDate === 'string') {
            const parsedDate = new Date(dueDate);
            if (!isNaN(parsedDate.getTime())) {
                dueDate = formatDate(parsedDate);
            }
        }
        if (!dueDate && $item("2").$node["INPUTC"]?.json?.posted_at) {
            const postedDate = new Date($item("2").$node["INPUTC"].json.posted_at);
            const dueDate = new Date(postedDate);
            dueDate.setDate(dueDate.getDate() + 5);
            dueDate = formatDate(dueDate);
        }
        
        const today = new Date();
        const [day, month, year] = dueDate.split('/');
        const dueDateObj = new Date(year, month - 1, day);
        const daysUntilDue = Math.ceil((dueDateObj - today) / (1000 * 60 * 60 * 24));
        
        const contentLines = task.content ? task.content.split('\n').filter(line => line.trim()) : [];
        const title = contentLines[0] || 'Untitled Task';
        const details = contentLines.slice(1).filter(l => l.trim());
        
        // Determine urgency and status
        let status = 'Low Priority';
        let urgency = 'normal';
        let sentiment = 'neutral';
        
        if (daysUntilDue < -3) {
            status = 'Overdue';
            urgency = 'critical';
            sentiment = 'disappointed';
        } else if (daysUntilDue <= -1) {
            status = 'Critical';
            urgency = 'high';
            sentiment = 'concerned';
        } else if (daysUntilDue === 0) {
            status = 'Due Today';
            urgency = 'high';
            sentiment = 'urgent';
        } else if (daysUntilDue <= 3) {
            status = 'Upcoming';
            urgency = 'medium';
            sentiment = 'attentive';
        }

        // Categorize task
        const text = `${title} ${task.description || ''}`.toLowerCase();
        let category = {
            type: 'General',
            subtype: 'Task',
            importance: 'normal'
        };

        // Financial tasks
        if (text.includes('tax') || text.includes('vat')) {
            category = {
                type: 'Financial',
                subtype: 'Tax',
                importance: 'high'
            };
            sentiment = 'focused';
        } else if (text.includes('payment') || text.includes('invoice')) {
            category = {
                type: 'Financial',
                subtype: 'Payment',
                importance: 'high'
            };
            sentiment = 'serious';
        }

        // Medical tasks
        if (text.includes('medical') || text.includes('health')) {
            category = {
                type: 'Medical',
                subtype: 'Health',
                importance: 'critical'
            };
            sentiment = 'caring';
        } else if (text.includes('doctor') || text.includes('appointment')) {
            category = {
                type: 'Medical',
                subtype: 'Appointment',
                importance: 'high'
            };
            sentiment = 'concerned';
        }

        // Vehicle tasks
        if (text.includes('car') || text.includes('rover') || text.includes('beetle')) {
            category = {
                type: 'Vehicle',
                subtype: 'Maintenance',
                importance: 'medium'
            };
            sentiment = 'practical';
        }

        // Home tasks
        if (text.includes('bulb') || text.includes('garage') || text.includes('house')) {
            category = {
                type: 'Home',
                subtype: 'Maintenance',
                importance: 'medium'
            };
            sentiment = 'helpful';
        }

        // Admin tasks
        if (text.includes('study') || text.includes('paper') || text.includes('file')) {
            category = {
                type: 'Admin',
                subtype: 'Documentation',
                importance: 'normal'
            };
            sentiment = 'organized';
        }

        const processedTask = {
            id: task.id,  // Todoist ID
            title,
            category,
            urgency,
            sentiment,
            is_completed: false,
            due: {
                date: dueDate,
                days_until: daysUntilDue,
                formatted: `${dueDate} (${Math.abs(daysUntilDue)} days ${daysUntilDue < 0 ? 'overdue' : 'remaining'})`
            },
            status,
            details,
            metadata: {
                description: task.description,
                labels: task.labels,
                comments: task.comments || ''
            }
        };

        // Pass through docid if it exists in original task
        if ('docid' in task) {
            processedTask.docid = task.docid;
        }

        return processedTask;
    })
    .sort((a, b) => {
        if (a.urgency !== b.urgency) {
            const priority = { critical: 0, high: 1, medium: 2, normal: 3 };
            return priority[a.urgency] - priority[b.urgency];
        }
        return a.due.days_until - b.due.days_until;
    });

// Get completed tasks separately
const completedTasks = tasks
    .filter(task => task.is_completed)
    .map(task => {
        const completedTask = {
            id: task.id,  // Todoist ID
            title: task.content.split('\n')[0] || 'Untitled Task',
            is_completed: true,
            metadata: {
                description: task.description,
                labels: task.labels,
                comments: task.comments || ''
            }
        };

        // Pass through docid if it exists in original task
        if ('docid' in task) {
            completedTask.docid = task.docid;
        }

        return completedTask;
    });

// Group tasks by category and urgency
const taskAnalysis = {
    by_category: {},
    by_urgency: {
        critical: [],
        high: [],
        medium: [],
        normal: []
    },
    by_sentiment: {},
    by_subtype: {},
    by_importance: {
        critical: [],
        high: [],
        medium: [],
        normal: []
    },
    overdue: [],
    due_today: [],
    due_this_week: [],
    by_time_range: {
        overdue_critical: [],
        overdue_high: [],
        due_today: [],
        due_tomorrow: [],
        due_this_week: [],
        due_next_week: [],
        future: []
    }
};

processedTasks.forEach(task => {
    // Group by category
    const categoryKey = task.category.type;
    if (!taskAnalysis.by_category[categoryKey]) {
        taskAnalysis.by_category[categoryKey] = [];
    }
    taskAnalysis.by_category[categoryKey].push(task);

    // Group by urgency
    taskAnalysis.by_urgency[task.urgency].push(task);

    // Group by sentiment
    if (!taskAnalysis.by_sentiment[task.sentiment]) {
        taskAnalysis.by_sentiment[task.sentiment] = [];
    }
    taskAnalysis.by_sentiment[task.sentiment].push(task);

    // Group by subtype
    const subtypeKey = task.category.subtype;
    if (!taskAnalysis.by_subtype[subtypeKey]) {
        taskAnalysis.by_subtype[subtypeKey] = [];
    }
    taskAnalysis.by_subtype[subtypeKey].push(task);

    // Group by importance
    taskAnalysis.by_importance[task.category.importance].push(task);

    // Track time-based categories
    if (task.due.days_until < 0) {
        taskAnalysis.overdue.push(task);
        if (task.urgency === 'critical') {
            taskAnalysis.by_time_range.overdue_critical.push(task);
        } else {
            taskAnalysis.by_time_range.overdue_high.push(task);
        }
    } else if (task.due.days_until === 0) {
        taskAnalysis.due_today.push(task);
        taskAnalysis.by_time_range.due_today.push(task);
    } else if (task.due.days_until === 1) {
        taskAnalysis.by_time_range.due_tomorrow.push(task);
    } else if (task.due.days_until <= 7) {
        taskAnalysis.due_this_week.push(task);
        taskAnalysis.by_time_range.due_this_week.push(task);
    } else if (task.due.days_until <= 14) {
        taskAnalysis.by_time_range.due_next_week.push(task);
    } else {
        taskAnalysis.by_time_range.future.push(task);
    }
});

// Generate detailed summaries
const summaries = {
    critical_summary: `${taskAnalysis.by_urgency.critical.length} critical tasks requiring immediate attention`,
    overdue_summary: `${taskAnalysis.overdue.length} tasks are overdue`,
    category_summary: Object.entries(taskAnalysis.by_category)
        .map(([category, tasks]) => `${tasks.length} ${category.toLowerCase()} tasks`)
        .join(', '),
    time_based_summary: {
        overdue: `${taskAnalysis.overdue.length} overdue tasks (${taskAnalysis.by_time_range.overdue_critical.length} critical)`,
        due_today: `${taskAnalysis.due_today.length} tasks due today`,
        this_week: `${taskAnalysis.due_this_week.length} tasks due this week`,
        next_week: `${taskAnalysis.by_time_range.due_next_week.length} tasks due next week`
    },
    category_details: Object.entries(taskAnalysis.by_category).map(([category, tasks]) => ({
        category,
        total: tasks.length,
        urgent: tasks.filter(t => t.urgency === 'critical' || t.urgency === 'high').length,
        overdue: tasks.filter(t => t.due.days_until < 0).length
    })),
    sentiment_distribution: Object.entries(taskAnalysis.by_sentiment).map(([sentiment, tasks]) => ({
        sentiment,
        count: tasks.length,
        categories: [...new Set(tasks.map(t => t.category.type))]
    }))
};

// Calculate trends and patterns
const trends = {
    most_urgent_category: Object.entries(taskAnalysis.by_category)
        .map(([category, tasks]) => ({
            category,
            urgent_count: tasks.filter(t => t.urgency === 'critical').length
        }))
        .sort((a, b) => b.urgent_count - a.urgent_count)[0],
    overdue_distribution: Object.entries(taskAnalysis.by_category)
        .map(([category, tasks]) => ({
            category,
            overdue_count: tasks.filter(t => t.due.days_until < 0).length,
            percentage: (tasks.filter(t => t.due.days_until < 0).length / tasks.length * 100).toFixed(1)
        })),
    category_importance: Object.entries(taskAnalysis.by_category)
        .map(([category, tasks]) => ({
            category,
            average_importance: tasks.reduce((acc, task) => {
                const importance = { critical: 3, high: 2, medium: 1, normal: 0 };
                return acc + importance[task.category.importance];
            }, 0) / tasks.length
        }))
};

// Return array of items for workflow branching
return [
    ...processedTasks.map(task => ({
        json: {
            ...task,
            is_completed: false
        }
    })),
    ...completedTasks.map(task => ({
        json: {
            ...task,
            is_completed: true
        }
    }))
];