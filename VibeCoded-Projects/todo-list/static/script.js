// Global variables
let tasks = [];
let categories = [];
let currentEditingTask = null;

// DOM elements
const taskList = document.getElementById('task-list');
const noTasksElement = document.getElementById('no-tasks');
const taskModal = document.getElementById('task-modal');
const categoryModal = document.getElementById('category-modal');
const taskForm = document.getElementById('task-form');
const categoryForm = document.getElementById('category-form');
const searchInput = document.getElementById('search-input');
const categoryFilter = document.getElementById('category-filter');
const priorityFilter = document.getElementById('priority-filter');
const statusFilter = document.getElementById('status-filter');
const sortBy = document.getElementById('sort-by');

// Initialize the app
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
    setupEventListeners();
});

function initializeApp() {
    loadCategories();
    loadTasks();
    loadStats();
    
    // Request notification permission
    if ('Notification' in window && Notification.permission === 'default') {
        Notification.requestPermission();
    }
    
    // Set up reminder checking
    setInterval(checkReminders, 60000); // Check every minute
}

function setupEventListeners() {
    // Modal controls
    document.getElementById('add-task-btn').addEventListener('click', () => openTaskModal());
    document.getElementById('add-category-btn').addEventListener('click', () => openCategoryModal());
    document.getElementById('modal-close').addEventListener('click', () => closeTaskModal());
    document.getElementById('category-modal-close').addEventListener('click', () => closeCategoryModal());
    document.getElementById('cancel-btn').addEventListener('click', () => closeTaskModal());
    document.getElementById('category-cancel-btn').addEventListener('click', () => closeCategoryModal());
    
    // Form submissions
    taskForm.addEventListener('submit', handleTaskSubmit);
    categoryForm.addEventListener('submit', handleCategorySubmit);
    
    // Filter and search
    searchInput.addEventListener('input', debounce(loadTasks, 300));
    categoryFilter.addEventListener('change', loadTasks);
    priorityFilter.addEventListener('change', loadTasks);
    statusFilter.addEventListener('change', loadTasks);
    sortBy.addEventListener('change', loadTasks);
    
    // Close modals when clicking outside
    taskModal.addEventListener('click', (e) => {
        if (e.target === taskModal) closeTaskModal();
    });
    
    categoryModal.addEventListener('click', (e) => {
        if (e.target === categoryModal) closeCategoryModal();
    });
    
    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeTaskModal();
            closeCategoryModal();
        }
        if (e.ctrlKey && e.key === 'n') {
            e.preventDefault();
            openTaskModal();
        }
    });
}

// API functions
async function apiCall(endpoint, method = 'GET', data = null) {
    const config = {
        method,
        headers: {
            'Content-Type': 'application/json',
        },
    };
    
    if (data) {
        config.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(`/api${endpoint}`, config);
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.error || 'An error occurred');
        }
        
        return response.status === 204 ? null : await response.json();
    } catch (error) {
        showNotification(error.message, 'error');
        throw error;
    }
}

// Task functions
async function loadTasks() {
    const params = new URLSearchParams();
    
    if (searchInput.value.trim()) params.append('search', searchInput.value.trim());
    if (categoryFilter.value) params.append('category_id', categoryFilter.value);
    if (priorityFilter.value) params.append('priority', priorityFilter.value);
    if (statusFilter.value) params.append('completed', statusFilter.value);
    if (sortBy.value) params.append('sort_by', sortBy.value);
    
    const queryString = params.toString();
    const endpoint = queryString ? `/tasks?${queryString}` : '/tasks';
    
    try {
        tasks = await apiCall(endpoint);
        renderTasks();
        loadStats();
    } catch (error) {
        console.error('Failed to load tasks:', error);
    }
}

function renderTasks() {
    if (tasks.length === 0) {
        taskList.innerHTML = '<div class="no-tasks" id="no-tasks"><i class="fas fa-clipboard-list"></i><p>No tasks found. Add your first task to get started!</p></div>';
        return;
    }
    
    taskList.innerHTML = tasks.map(task => createTaskHTML(task)).join('');
}

function createTaskHTML(task) {
    const dueDate = task.due_date ? new Date(task.due_date) : null;
    const isOverdue = dueDate && dueDate < new Date() && !task.completed;
    const category = categories.find(cat => cat.id === task.category_id);
    
    return `
        <div class="task-item ${task.completed ? 'completed' : ''}" data-task-id="${task.id}">
            <div class="task-header">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <button class="task-toggle ${task.completed ? 'completed' : ''}" onclick="toggleTask(${task.id})">
                        <i class="fas ${task.completed ? 'fa-check-circle' : 'fa-circle'}"></i>
                    </button>
                    <h4 class="task-title">${escapeHtml(task.title)}</h4>
                </div>
                <div class="task-actions">
                    <button class="btn btn-secondary" onclick="editTask(${task.id})">
                        <i class="fas fa-edit"></i>
                    </button>
                    <button class="btn btn-danger" onclick="deleteTask(${task.id})">
                        <i class="fas fa-trash"></i>
                    </button>
                </div>
            </div>
            
            ${task.description ? `<p class="task-description">${escapeHtml(task.description)}</p>` : ''}
            
            <div class="task-meta">
                <span class="task-priority ${task.priority}">${task.priority.toUpperCase()}</span>
                
                ${category ? `<span class="task-category" style="background-color: ${category.color}">${category.name}</span>` : ''}
                
                ${dueDate ? `
                    <span class="task-due-date ${isOverdue ? 'overdue' : ''}">
                        <i class="fas fa-calendar"></i>
                        ${formatDate(dueDate)} ${isOverdue ? '(Overdue!)' : ''}
                    </span>
                ` : ''}
                
                ${task.reminder_time ? `
                    <span class="task-reminder">
                        <i class="fas fa-bell"></i>
                        ${formatDateTime(new Date(task.reminder_time))}
                    </span>
                ` : ''}
            </div>
        </div>
    `;
}

async function toggleTask(taskId) {
    try {
        const updatedTask = await apiCall(`/tasks/${taskId}/toggle`, 'PATCH');
        const taskIndex = tasks.findIndex(t => t.id === taskId);
        if (taskIndex !== -1) {
            tasks[taskIndex] = updatedTask;
            renderTasks();
            loadStats();
        }
        showNotification(`Task ${updatedTask.completed ? 'completed' : 'reopened'}!`, 'success');
    } catch (error) {
        console.error('Failed to toggle task:', error);
    }
}

async function deleteTask(taskId) {
    if (!confirm('Are you sure you want to delete this task?')) return;
    
    try {
        await apiCall(`/tasks/${taskId}`, 'DELETE');
        tasks = tasks.filter(t => t.id !== taskId);
        renderTasks();
        loadStats();
        showNotification('Task deleted successfully!', 'success');
    } catch (error) {
        console.error('Failed to delete task:', error);
    }
}

function editTask(taskId) {
    const task = tasks.find(t => t.id === taskId);
    if (!task) return;
    
    currentEditingTask = task;
    
    // Populate form
    document.getElementById('task-title').value = task.title;
    document.getElementById('task-description').value = task.description || '';
    document.getElementById('task-category').value = task.category_id || '';
    document.getElementById('task-priority').value = task.priority;
    document.getElementById('task-due-date').value = task.due_date || '';
    
    if (task.reminder_time) {
        const reminderDate = new Date(task.reminder_time);
        document.getElementById('task-reminder').value = formatDateTimeLocal(reminderDate);
    } else {
        document.getElementById('task-reminder').value = '';
    }
    
    document.getElementById('modal-title').textContent = 'Edit Task';
    document.getElementById('save-btn').textContent = 'Update Task';
    
    openTaskModal();
}

// Category functions
async function loadCategories() {
    try {
        categories = await apiCall('/categories');
        renderCategories();
        updateCategorySelects();
    } catch (error) {
        console.error('Failed to load categories:', error);
    }
}

function renderCategories() {
    const categoryList = document.getElementById('category-list');
    categoryList.innerHTML = categories.map(category => `
        <div class="category-item" style="background-color: ${category.color}">
            <span>${escapeHtml(category.name)}</span>
            <span class="task-count">${category.task_count}</span>
            <button class="delete-category" onclick="deleteCategory(${category.id})" title="Delete category">
                <i class="fas fa-times"></i>
            </button>
        </div>
    `).join('');
}

function updateCategorySelects() {
    const categoryOptions = categories.map(cat => 
        `<option value="${cat.id}">${escapeHtml(cat.name)}</option>`
    ).join('');
    
    document.getElementById('task-category').innerHTML = 
        '<option value="">No Category</option>' + categoryOptions;
    
    document.getElementById('category-filter').innerHTML = 
        '<option value="">All Categories</option>' + categoryOptions;
}

async function deleteCategory(categoryId) {
    if (!confirm('Are you sure you want to delete this category? Tasks in this category will become uncategorized.')) return;
    
    try {
        await apiCall(`/categories/${categoryId}`, 'DELETE');
        categories = categories.filter(c => c.id !== categoryId);
        renderCategories();
        updateCategorySelects();
        loadTasks(); // Reload tasks to update display
        showNotification('Category deleted successfully!', 'success');
    } catch (error) {
        console.error('Failed to delete category:', error);
    }
}

// Modal functions
function openTaskModal() {
    if (!currentEditingTask) {
        // Reset form for new task
        taskForm.reset();
        document.getElementById('modal-title').textContent = 'Add New Task';
        document.getElementById('save-btn').textContent = 'Save Task';
        document.getElementById('task-priority').value = 'medium';
    }
    
    taskModal.classList.add('show');
    document.getElementById('task-title').focus();
}

function closeTaskModal() {
    taskModal.classList.remove('show');
    currentEditingTask = null;
    taskForm.reset();
}

function openCategoryModal() {
    categoryForm.reset();
    document.getElementById('category-color').value = '#007bff';
    categoryModal.classList.add('show');
    document.getElementById('category-name').focus();
}

function closeCategoryModal() {
    categoryModal.classList.remove('show');
    categoryForm.reset();
}

// Form handlers
async function handleTaskSubmit(e) {
    e.preventDefault();
    
    const formData = new FormData(taskForm);
    const taskData = {
        title: document.getElementById('task-title').value.trim(),
        description: document.getElementById('task-description').value.trim(),
        priority: document.getElementById('task-priority').value,
        category_id: document.getElementById('task-category').value || null,
        due_date: document.getElementById('task-due-date').value || null,
        reminder_time: document.getElementById('task-reminder').value || null
    };
    
    // Convert reminder_time to ISO format if provided
    if (taskData.reminder_time) {
        taskData.reminder_time = new Date(taskData.reminder_time).toISOString();
    }
    
    try {
        if (currentEditingTask) {
            // Update existing task
            const updatedTask = await apiCall(`/tasks/${currentEditingTask.id}`, 'PUT', taskData);
            const taskIndex = tasks.findIndex(t => t.id === currentEditingTask.id);
            if (taskIndex !== -1) {
                tasks[taskIndex] = updatedTask;
            }
            showNotification('Task updated successfully!', 'success');
        } else {
            // Create new task
            const newTask = await apiCall('/tasks', 'POST', taskData);
            tasks.unshift(newTask);
            showNotification('Task created successfully!', 'success');
        }
        
        renderTasks();
        loadStats();
        closeTaskModal();
    } catch (error) {
        console.error('Failed to save task:', error);
    }
}

async function handleCategorySubmit(e) {
    e.preventDefault();
    
    const categoryData = {
        name: document.getElementById('category-name').value.trim(),
        color: document.getElementById('category-color').value
    };
    
    try {
        const newCategory = await apiCall('/categories', 'POST', categoryData);
        categories.push(newCategory);
        renderCategories();
        updateCategorySelects();
        closeCategoryModal();
        showNotification('Category created successfully!', 'success');
    } catch (error) {
        console.error('Failed to create category:', error);
    }
}

// Stats
async function loadStats() {
    try {
        const stats = await apiCall('/stats');
        document.getElementById('total-tasks').textContent = stats.total_tasks;
        document.getElementById('pending-tasks').textContent = stats.pending_tasks;
        document.getElementById('completed-tasks').textContent = stats.completed_tasks;
        document.getElementById('overdue-tasks').textContent = stats.overdue_tasks;
    } catch (error) {
        console.error('Failed to load stats:', error);
    }
}

// Reminders
function checkReminders() {
    const now = new Date();
    
    tasks.forEach(task => {
        if (task.reminder_time && !task.completed) {
            const reminderTime = new Date(task.reminder_time);
            const timeDiff = reminderTime.getTime() - now.getTime();
            
            // Show notification if reminder is within 1 minute
            if (timeDiff > 0 && timeDiff <= 60000) {
                showReminderNotification(task);
            }
        }
    });
}

function showReminderNotification(task) {
    if ('Notification' in window && Notification.permission === 'granted') {
        const notification = new Notification('Task Reminder', {
            body: `Don't forget: ${task.title}`,
            icon: '/static/favicon.ico',
            badge: '/static/favicon.ico'
        });
        
        notification.onclick = function() {
            window.focus();
            notification.close();
            
            // Scroll to task
            const taskElement = document.querySelector(`[data-task-id="${task.id}"]`);
            if (taskElement) {
                taskElement.scrollIntoView({ behavior: 'smooth' });
                taskElement.style.animation = 'pulse 1s';
            }
        };
        
        // Auto close after 5 seconds
        setTimeout(() => notification.close(), 5000);
    } else {
        // Fallback to in-app notification
        showNotification(`Reminder: ${task.title}`, 'info');
    }
}

// Utility functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function formatDate(date) {
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function formatDateTime(date) {
    return date.toLocaleString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    });
}

function formatDateTimeLocal(date) {
    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    
    return `${year}-${month}-${day}T${hours}:${minutes}`;
}

function showNotification(message, type = 'success') {
    const container = document.getElementById('notification-container');
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.innerHTML = `
        <div style="display: flex; align-items: center; gap: 10px;">
            <i class="fas ${getNotificationIcon(type)}"></i>
            <span>${escapeHtml(message)}</span>
        </div>
    `;
    
    container.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    }, 5000);
    
    // Remove on click
    notification.addEventListener('click', () => {
        if (notification.parentNode) {
            notification.parentNode.removeChild(notification);
        }
    });
}

function getNotificationIcon(type) {
    switch (type) {
        case 'success': return 'fa-check-circle';
        case 'error': return 'fa-exclamation-circle';
        case 'warning': return 'fa-exclamation-triangle';
        case 'info': return 'fa-info-circle';
        default: return 'fa-info-circle';
    }
}

// Local Storage functions for offline support
function saveToLocalStorage() {
    try {
        localStorage.setItem('todo-tasks', JSON.stringify(tasks));
        localStorage.setItem('todo-categories', JSON.stringify(categories));
    } catch (error) {
        console.warn('Failed to save to localStorage:', error);
    }
}

function loadFromLocalStorage() {
    try {
        const savedTasks = localStorage.getItem('todo-tasks');
        const savedCategories = localStorage.getItem('todo-categories');
        
        if (savedTasks) tasks = JSON.parse(savedTasks);
        if (savedCategories) categories = JSON.parse(savedCategories);
    } catch (error) {
        console.warn('Failed to load from localStorage:', error);
    }
}

// Auto-save to localStorage when data changes
function setupAutoSave() {
    // Save tasks and categories to localStorage whenever they change
    const originalApiCall = apiCall;
    window.apiCall = async function(...args) {
        const result = await originalApiCall.apply(this, args);
        saveToLocalStorage();
        return result;
    };
}

// Initialize auto-save
setupAutoSave();
