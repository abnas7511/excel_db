// Handle file upload
document.getElementById('uploadForm').addEventListener('submit', function (event) {
    event.preventDefault();
    let formData = new FormData();
    let fileInput = document.getElementById('fileInput');
    formData.append('file', fileInput.files[0]);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('uploadStatus').innerText = "Error: " + data.error;
        } else {
            document.getElementById('uploadStatus').innerText = "Success: " + data.message;
        }
    })
    .catch(err => {
        document.getElementById('uploadStatus').innerText = "Error: " + err.message;
    });
});

// Handle single user addition
document.getElementById('addUserForm').addEventListener('submit', function (event) {
    event.preventDefault();
    let user = document.getElementById('user').value;
    let emailid = document.getElementById('emailid').value;
    let role = document.getElementById('role').value;
    let application_mapped = document.getElementById('application_mapped').value;
    let license_type = document.getElementById('license_type').value;

    let data = {
        user: user,
        emailid: emailid,
        role: role,
        application_mapped: application_mapped,
        license_type: license_type
    };

    fetch('/users', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('addUserStatus').innerText = "Error: " + data.error;
        } else {
            document.getElementById('addUserStatus').innerText = "User added successfully: " + data.message;
        }
    })
    .catch(err => {
        document.getElementById('addUserStatus').innerText = "Error: " + err.message;
    });
});

// Handle user deletion
document.getElementById('deleteUserForm').addEventListener('submit', function (event) {
    event.preventDefault();
    let userId = document.getElementById('deleteUserId').value;

    fetch(`/users/${userId}`, {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('deleteStatus').innerText = "Error: " + data.error;
        } else {
            document.getElementById('deleteStatus').innerText = "User deleted successfully: " + data.message;
        }
    })
    .catch(err => {
        document.getElementById('deleteStatus').innerText = "Error: " + err.message;
    });
});

// Handle user update
document.getElementById('updateUserForm').addEventListener('submit', function (event) {
    event.preventDefault();
    let userId = document.getElementById('updateUserId').value;
    let user = document.getElementById('updateUserName').value;
    let emailid = document.getElementById('updateEmailId').value;
    let role = document.getElementById('updateRole').value;
    let application_mapped = document.getElementById('updateApplicationMapped').value;
    let license_type = document.getElementById('updateLicenseType').value;

    let data = {
        user: user || undefined,
        emailid: emailid || undefined,
        role: role || undefined,
        application_mapped: application_mapped || undefined,
        license_type: license_type || undefined
    };

    fetch(`/users/${userId}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('updateStatus').innerText = "Error: " + data.error;
        } else {
            document.getElementById('updateStatus').innerText = "User updated successfully: " + data.message;
        }
    })
    .catch(err => {
        document.getElementById('updateStatus').innerText = "Error: " + err.message;
    });
});

// Handle fetching all users
document.getElementById('fetchUsersButton').addEventListener('click', function () {
    fetch('/users')
    .then(response => response.json())
    .then(data => {
        const usersList = document.getElementById('usersList');
        usersList.innerHTML = '';  // Clear previous results
        data.forEach(user => {
            const listItem = document.createElement('li');
            listItem.innerText = `User: ${user.user}, Email: ${user.emailid}, Role: ${user.role}, Application: ${user.application_mapped}, License: ${user.license_type}`;
            usersList.appendChild(listItem);
        });
    })
    .catch(err => {
        document.getElementById('usersList').innerText = "Error: " + err.message;
    });
});
