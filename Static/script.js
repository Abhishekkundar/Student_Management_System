// 🔹 Select Role for Login
function selectRole(role) {
    document.getElementById('roleInput').value = role;
    
    // Remove active class from all buttons
    document.querySelectorAll('.role-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Add active class to selected button
    document.querySelector(`[data-role="${role}"]`).classList.add('active');
}

// 🔹 Validate Login Form
function validateForm() {
    const email = document.querySelector('input[name="email"]').value.trim();
    const password = document.querySelector('input[name="password"]').value.trim();
    const role = document.getElementById('roleInput').value;

    if (!email) {
        alert('Please enter your email address');
        return false;
    }
    
    if (!password) {
        alert('Please enter your password');
        return false;
    }
    
    if (!role) {
        alert('Please select a role');
        return false;
    }
    
    alert(`Login successful as ${role}!`);
    return true;
}

// Load students on page load
window.onload = function () {
    if (document.getElementById("tableBody")) {
        loadStudents();
    }
};

// 🔹 Load & Render Students
async function loadStudents() {
    try {
        let res = await fetch("/api/students");
        let data = await res.json();

        let table = document.getElementById("tableBody");
        table.innerHTML = "";

        for (let id in data) {
            table.innerHTML += `
            <tr>
                <td>${id}</td>
                <td>${data[id].name}</td>
                <td>${data[id].Total_marks}</td>
                <td>${data[id].Percentage}%</td>
                <td><span class="badge ${data[id].Grade.toLowerCase()}">${data[id].Grade}</span></td>
                <td>
                    <button class="btn-delete" onclick="deleteStudent('${id}')">Delete</button>
                </td>
            </tr>`;
        }

        // Update Dashboard Stats
        updateDashboardStats(data);

    } catch (error) {
        console.error("Error loading students:", error);
    }
}

// 🔹 Helper: Add Dynamic Subject Row
function addSubjectRow() {
    const container = document.getElementById('subjectContainer');
    const newRow = document.createElement('div');
    newRow.className = 'form-row subject-row';
    newRow.innerHTML = `
        <div class="form-input-group">
            <input type="text" class="sub-name" placeholder="Subject Name" required>
        </div>
        <div class="form-input-group">
            <input type="number" class="sub-marks" placeholder="Marks" min="0" max="100" required>
        </div>
        <button type="button" class="btn-remove" onclick="this.parentElement.remove()">×</button>
    `;
    container.appendChild(newRow);
}

// 🔹 Add Student (Updated for Dynamic Data)
async function addStudent() {
    const id = document.getElementById("id").value;
    const name = document.getElementById("name").value;
    const department = document.getElementById("department").value;

    // Gather dynamic subjects
    let subjects_list = [];
    let totalMarks = 0;
    let rows = document.querySelectorAll('.subject-row');

    rows.forEach(row => {
        let subName = row.querySelector('.sub-name').value;
        let subMarks = parseInt(row.querySelector('.sub-marks').value) || 0;
        if (subName) {
            subjects_list.push({ subject:subName,
                marks:subMarks });
            totalMarks += subMarks;
        }
    });
    if (!id || !name || subjects_list.length === 0) {
        alert("Please fill all fields and add at least one subject!");
        return;
    }

    try {
        let res = await fetch("/api/add", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ 
                id, 
                name, 
                department, 
                subjects_list
                
            })
        });

        if (res.ok) {
            alert("Student Registered ✅");
            resetForm();
            showSection('view');
        } else {
            const error = await res.json();
            alert(error.error);
        }
    } catch (error) {
        console.error("Error:", error);
    }
}

// 🔹 Helper: Update Dashboard Stats
function updateDashboardStats(data) {
    const totalEl = document.getElementById("total");
    const avgEl = document.getElementById("avg-percent");
    const students = Object.values(data);

    if (totalEl) totalEl.innerText = students.length;

    if (avgEl) {
        const totalPercentage = students.reduce((sum, student) => {
            return sum + Number(student.Percentage || 0);
        }, 0);
        const average = students.length ? totalPercentage / students.length : 0;
        avgEl.innerText = `${average.toFixed(2)}%`;
    }
}

// 🔹 Helper: Reset Form
function resetForm() {
    document.getElementById("studentForm").reset();
    document.getElementById("subjectContainer").innerHTML = ""; // Clear dynamic rows
    addSubjectRow(); // Add one blank row back
}

// 🔹 Delete & Section Switch logic remains same...
function showSection(id) {
    document.querySelectorAll(".section").forEach(sec => sec.classList.add("hidden"));
    document.getElementById(id).classList.remove("hidden");
    if (id === "view") loadStudents();
}

async function deleteStudent(id) {
    if (!confirm("Are you sure?")) return;
    const res = await fetch(`/api/delete/${id}`, { method: "DELETE" });
    if (res.ok) {
        loadStudents();
    } else {
        const error = await res.json();
        alert(error.error);
    }
}
