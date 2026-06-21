const STATUS_LABELS = {
    open: "Open",
    in_progress: "In Progress",
    done: "Done",
    cancelled: "Cancelled",
};

const STATUS_OPTIONS = ["open", "in_progress", "done", "cancelled"];

const createForm = document.getElementById("create-form");
const titleInput = document.getElementById("title");
const descriptionInput = document.getElementById("description");
const statusFilter = document.getElementById("status-filter");
const refreshBtn = document.getElementById("refresh-btn");
const taskList = document.getElementById("task-list");
const emptyState = document.getElementById("empty-state");

function formatStatus(status) {
    return STATUS_LABELS[status] || status;
}

function formatDate(isoString) {
    if (!isoString) {
        return "Unknown";
    }
    return new Date(isoString).toLocaleString();
}

async function apiRequest(url, options = {}) {
    const response = await fetch(url, {
        headers: {
            "Content-Type": "application/json",
            ...(options.headers || {}),
        },
        ...options,
    });

    if (!response.ok) {
        let detail = "Request failed";
        try {
            const data = await response.json();
            detail = data.detail || detail;
        } catch (_error) {
            // Ignore JSON parse errors for empty responses.
        }
        throw new Error(detail);
    }

    if (response.status === 204) {
        return null;
    }

    return response.json();
}

function buildTasksUrl() {
    const status = statusFilter.value;
    if (status) {
        return `/api/tasks?status=${encodeURIComponent(status)}`;
    }
    return "/api/tasks";
}

function renderTasks(tasks) {
    taskList.innerHTML = "";

    if (!tasks.length) {
        emptyState.classList.remove("hidden");
        return;
    }

    emptyState.classList.add("hidden");

    for (const task of tasks) {
        const card = document.createElement("article");
        card.className = "task-card";
        card.innerHTML = `
            <h3>${escapeHtml(task.title)}</h3>
            <p class="task-description">${escapeHtml(task.description || "No description")}</p>
            <div class="task-meta">
                <span class="status-badge status-${task.status}">
                    Status: ${formatStatus(task.status)}
                </span>
                <span>Created: ${formatDate(task.created_at)}</span>
            </div>
            <div class="task-actions">
                <button type="button" class="btn btn-secondary btn-small" data-action="edit">
                    Edit
                </button>
                <button type="button" class="btn btn-primary btn-small" data-action="done">
                    Done
                </button>
                <button type="button" class="btn btn-danger btn-small" data-action="delete">
                    Delete
                </button>
            </div>
        `;

        card.querySelector('[data-action="edit"]').addEventListener("click", () => {
            editTask(task);
        });
        card.querySelector('[data-action="done"]').addEventListener("click", () => {
            markDone(task.id);
        });
        card.querySelector('[data-action="delete"]').addEventListener("click", () => {
            deleteTask(task.id, task.title);
        });

        taskList.appendChild(card);
    }
}

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
}

async function loadTasks() {
    try {
        const tasks = await apiRequest(buildTasksUrl());
        renderTasks(tasks);
    } catch (error) {
        alert(error.message);
    }
}

async function createTask(event) {
    event.preventDefault();

    const payload = {
        title: titleInput.value.trim(),
        description: descriptionInput.value.trim() || null,
    };

    if (!payload.title) {
        return;
    }

    try {
        await apiRequest("/api/tasks", {
            method: "POST",
            body: JSON.stringify(payload),
        });
        createForm.reset();
        await loadTasks();
    } catch (error) {
        alert(error.message);
    }
}

async function editTask(task) {
    const title = prompt("Task title", task.title);
    if (title === null) {
        return;
    }

    const description = prompt("Task description", task.description || "");
    if (description === null) {
        return;
    }

    const statusPrompt = prompt(
        `Task status (${STATUS_OPTIONS.join(", ")})`,
        task.status,
    );
    if (statusPrompt === null) {
        return;
    }

    const status = statusPrompt.trim();
    if (!STATUS_OPTIONS.includes(status)) {
        alert("Invalid status value.");
        return;
    }

    const payload = {
        title: title.trim(),
        description: description.trim() || null,
        status,
    };

    if (!payload.title) {
        alert("Title is required.");
        return;
    }

    try {
        await apiRequest(`/api/tasks/${task.id}`, {
            method: "PATCH",
            body: JSON.stringify(payload),
        });
        await loadTasks();
    } catch (error) {
        alert(error.message);
    }
}

async function deleteTask(taskId, title) {
    const confirmed = confirm(`Delete task "${title}"?`);
    if (!confirmed) {
        return;
    }

    try {
        await apiRequest(`/api/tasks/${taskId}`, { method: "DELETE" });
        await loadTasks();
    } catch (error) {
        alert(error.message);
    }
}

async function markDone(taskId) {
    try {
        await apiRequest(`/api/tasks/${taskId}/done`, { method: "POST" });
        await loadTasks();
    } catch (error) {
        alert(error.message);
    }
}

createForm.addEventListener("submit", createTask);
statusFilter.addEventListener("change", loadTasks);
refreshBtn.addEventListener("click", loadTasks);

loadTasks();
