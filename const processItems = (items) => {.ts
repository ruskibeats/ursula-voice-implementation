import {
    IExecuteFunctions,
    INodeExecutionData,
    INodeType,
    INodeTypeDescription,
    NodeConnectionType,
    NodeOperationError,
    IDataObject
} from 'n8n-workflow';

interface ITaskProperties extends IDataObject {
    docid: string;
    id?: string;
    'Due Date'?: string;
    content?: string;
    description?: string;
    labels?: string | string[];
    Order?: number;
    Comments?: string;
    is_completed?: boolean;
    isUrgent?: boolean;
    type?: string;
    daysUntilDue?: number;
    details?: string[];
    title?: string;
}

interface IEnrichedTask extends ITaskProperties {
    dueDate: string;
    status: string;
    type: string;
    details: string[];
    daysUntilDue: number;
    priorityScore: number;
    complexity: {
        level: string;
        estimatedTimeMinutes: number;
    };
    ssml: string;
    requiredActions: Record<string, boolean>;
}

interface ISSMLPattern {
    Type: string;
    Name: string;
    Pattern: string;
    Description: string;
}

const defaultSSMLPattern: ISSMLPattern = {
    Type: "emotion",
    Name: "happy",
    Pattern: "<amazon:emotion name=\"happy\" intensity=\"high\">$TEXT</amazon:emotion>",
    Description: "For excited, joyful moments"
};

export class TaskProcessor implements INodeType {
    description: INodeTypeDescription = {
        displayName: 'Task Processor',
        name: 'taskProcessor',
        group: ['transform'],
        version: 1,
        description: 'Process and analyze tasks with SSML support',
        defaults: {
            name: 'Task Processor',
        },
        properties: [
            {
                displayName: 'Operation',
                name: 'operation',
                type: 'string',
                default: 'process',
                description: 'The operation to perform',
                options: [
                    {
                        name: 'Process Tasks',
                        value: 'process',
                        description: 'Process and analyze tasks',
                    },
                ],
            },
        ],
        inputs: [{
            displayName: 'Input',
            type: NodeConnectionType.Main,
            required: true,
        }],
        outputs: [{
            displayName: 'Output',
            type: NodeConnectionType.Main,
        }],
    };

    async execute(this: IExecuteFunctions): Promise<INodeExecutionData[][]> {
        try {
            const items = this.getInputData();
            const returnData: INodeExecutionData[] = [];

            const processedItems = items.map((item) => {
                const json = item.json as ITaskProperties;
                if (!json || !json.docid || !json['Due Date']) {
                    return { json: { error: 'Invalid task data' } };
                }
                return { json };
            });

            const processor = new TaskProcessor();
            const result = processor.processItems(processedItems);
            returnData.push(...result);

            return [returnData];
        } catch (error) {
            if (error instanceof Error) {
                throw new Error(`Error processing tasks: ${error.message}`);
            }
            throw error;
        }
    }

    private getPriorityScore(task: ITaskProperties): number {
        let score = 0;
        score += task.isUrgent ? 100 : 0;
        score += typeof task.daysUntilDue === 'number' && task.daysUntilDue < 0 ? Math.abs(task.daysUntilDue * 2) : 0;
        score += task.type === 'Medical' ? 50 : 0;
        score += task.type === 'Financial' ? 40 : 0;
        return score;
    }

    private getComplexity(task: ITaskProperties) {
        const details = Array.isArray(task.details) ? task.details : [];
        const steps = details.length;
        const description = String(task.description || '');
        const hasDeadlines = description.includes('deadline') || description.includes('due by');
        const requiresDocuments = description.toLowerCase().includes('document') || description.includes('form');
        return {
            level: steps > 3 ? 'High' : steps > 1 ? 'Medium' : 'Low',
            requiresDocuments,
            hasDeadlines,
            estimatedTimeMinutes: steps * 30
        };
    }

    private getRequiredActions(task: ITaskProperties) {
        const text = `${task.title || ''} ${task.description || ''}`.toLowerCase();
        return {
            needsPayment: text.includes('pay') || text.includes('payment'),
            needsContact: text.includes('contact') || text.includes('call') || text.includes('email'),
            needsSubmission: text.includes('submit') || text.includes('file') || text.includes('send'),
            needsReview: text.includes('review') || text.includes('check')
        };
    }

    private processItems(items: INodeExecutionData[]): INodeExecutionData[] {
        if (!Array.isArray(items) || !items.length) return [];

        const ssmlPattern = defaultSSMLPattern;
        const uniqueTasks = new Map<string, IEnrichedTask>();

        items.forEach(item => {
            const task = item.json as ITaskProperties;
            if (!task || !task.docid || !task.content || !task['Due Date']) return;

            if (!uniqueTasks.has(task.docid)) {
                try {
                    const contentLines = task.content.split('\n').filter(line => line.trim());
                    const labels = typeof task.labels === 'string' ? JSON.parse(task.labels) : task.labels;
                    
                    const today = new Date();
                    const [day, month, year] = task['Due Date'].split('/');
                    const dueDateObj = new Date(year, month - 1, day);
                    const daysUntilDue = Math.ceil((dueDateObj - today) / (1000 * 60 * 60 * 24));
                    
                    let status = 'Low Priority';
                    let isUrgent = false;
                    
                    if (daysUntilDue < -3) {
                        status = 'Overdue';
                        isUrgent = true;
                    } else if (daysUntilDue <= -1) {
                        status = 'Critical';
                        isUrgent = true;
                    } else if (daysUntilDue === 0) {
                        status = 'High Priority';
                        isUrgent = true;
                    } else if (daysUntilDue <= 3) {
                const contentLines = typeof task.content === 'string' ? 
                    task.content.split('\n').filter(line => line.trim()) : [];
                const labels = task.labels ? 
                    (typeof task.labels === 'string' ? JSON.parse(task.labels) : task.labels) : [];

                const today = new Date();
                const [day, month, year] = (task['Due Date'] as string).split('/');
                const dueDateObj = new Date(parseInt(year), parseInt(month) - 1, parseInt(day));
                const daysUntilDue = Math.ceil((dueDateObj.getTime() - today.getTime()) / (1000 * 60 * 60 * 24));

                let status = 'Low Priority';
                let isUrgent = false;

                if (daysUntilDue < -3) {
                    status = 'Overdue';
                    isUrgent = true;
                } else if (daysUntilDue <= -1) {
                    status = 'Critical';
                    isUrgent = true;
                } else if (daysUntilDue === 0) {
                    status = 'High Priority';
                    isUrgent = true;
                } else if (daysUntilDue <= 3) {
                    status = 'Medium Priority';
                }

                const text = `${contentLines[0] || ''} ${task.description || ''}`.toLowerCase();
                let type = 'General';
                if (text.includes('tax') || text.includes('vat') || text.includes('payment')) type = 'Financial';
                if (text.includes('car') || text.includes('rover') || text.includes('beetle')) type = 'Vehicle';
                if (text.includes('medical') || text.includes('health') || text.includes('doctor') || text.includes('screening')) type = 'Medical';
                if (text.includes('bulb') || text.includes('garage') || text.includes('house')) type = 'Home';
                if (text.includes('study') || text.includes('paper') || text.includes('file')) type = 'Admin';

                const ssmlText = ssmlPattern.Pattern.replace('$TEXT', contentLines[0] || 'Untitled Task');

                const enrichedTask: IEnrichedTask = {
                    ...task,
                    dueDate: task['Due Date'],
                    status,
                    isUrgent,
                    type,
                    details: contentLines.slice(1).filter(l => l.trim()),
                    daysUntilDue,
                    order: task.Order || 0,
                    labels,
                    comments: task.Comments || '',
                    completed: task.is_completed || false,
                    ssml: ssmlText,
                    priorityScore: this.getPriorityScore(task),
                    complexity: this.getComplexity(task),
                    requiredActions: this.getRequiredActions(task)
                };

                uniqueTasks.set(task.docid, enrichedTask);
            }
        });

        const analyzedTasks = Array.from(uniqueTasks.values())
            .sort((a, b) => b.priorityScore - a.priorityScore);
        
        const urgentTasks = analyzedTasks.filter(task => task.isUrgent);
        const regularTasks = analyzedTasks.filter(task => !task.isUrgent);

        const formatTasks = (taskList: IEnrichedTask[]) => taskList
            .map(task => {
                const detailsText = task.details?.length ? 
                    `Details:\n${task.details.map(d => `- ${d}`).join('\n')}\n` : '';
                const complexityInfo = `Complexity: ${task.complexity.level} (Est. ${task.complexity.estimatedTimeMinutes} mins)`;
                const actionsNeeded = Object.entries(task.requiredActions)
                    .filter(([, needed]) => needed)
                    .map(([action]) => action.replace('needs', ''))
                    .join(', ');
                
                return `Task: ${task.ssml}\n` +
                       `Due: ${task.dueDate}${task.daysUntilDue ? ` (${Math.abs(task.daysUntilDue)} days ${task.daysUntilDue < 0 ? 'overdue' : 'remaining'})` : ''}\n` +
                       `Status: ${task.status}\n` +
                       `Type: ${task.type}\n` +
                       `${complexityInfo}\n` +
                       `Priority Score: ${task.priorityScore}\n` +
                       (actionsNeeded ? `Actions Needed: ${actionsNeeded}\n` : '') +
                       detailsText;
            }).join("\n---\n\n");

        const output = `Total Tasks: ${analyzedTasks.length}\n` +
                      `Urgent Tasks: ${urgentTasks.length}\n` +
                      `Regular Tasks: ${regularTasks.length}\n\n` +
                      (urgentTasks.length ? '🚨 URGENT TASKS:\n\n' + formatTasks(urgentTasks) : '') +
                      (regularTasks.length ? '\n📋 REGULAR TASKS:\n\n' + formatTasks(regularTasks) : '');

        const typeFrequencies: Record<string, number> = analyzedTasks.reduce((types, task) => {
            types[task.type] = (types[task.type] || 0) + 1;
            return types;
        }, {} as Record<string, number>);

        const mostCommonType = Object.entries(typeFrequencies)
            .sort(([, a], [, b]) => b - a)
            .shift()?.[0] || 'General';

        return [{
            json: {
                text: output,
                stats: {
                    total: analyzedTasks.length,
                    urgent: urgentTasks.length,
                    regular: regularTasks.length
                },
                urgentTasks,
                regularTasks,
                pattern: ssmlPattern,
                metadata: {
                    processedAt: new Date().toISOString(),
                    totalPriorityScore: analyzedTasks.reduce((sum, task) => sum + task.priorityScore, 0),
                    averageComplexity: analyzedTasks.length ? 
                        analyzedTasks.reduce((sum, task) => {
                            return sum + (task.complexity.level === 'High' ? 3 : task.complexity.level === 'Medium' ? 2 : 1);
                        }, 0) / analyzedTasks.length : 0,
                    mostCommonType,
                    typeDistribution: typeFrequencies
                }
            }
        }];
    }
}