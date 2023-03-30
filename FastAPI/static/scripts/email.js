// Function to get the list of files from the server and display them on the page
function getFiles() {
    fetch("/get_files")
        .then(response => response.json())
        .then(data => {
            const fileList = document.getElementById("fileList");
            data.files.forEach(file => {
                const li = document.createElement("li");
                li.innerText = file;
                fileList.appendChild(li);
            });
        })
        .catch(error => console.error(error));
}

// Function to send an email with the training data
function sendEmail() {
    const email = document.getElementById("emailInput").value;

    if (email === "") {
        alert("Please enter an email address");
        return;
    }

    // Disable the submit button
    document.getElementById("submitButton").disabled = true;

    // Display a loading message
    document.getElementById("filesPreview").innerHTML = "<p>Loading...</p>";

    // Send a request to the server to create and send the zip file
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/send_zip_file");
    xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4) {
            if (xhr.status === 200) {
                // Display a success message
                document.getElementById("filesPreview").innerHTML = "<p>Email sent successfully!</p>";
            } else {
                // Display an error message
                document.getElementById("filesPreview").innerHTML = "<p>An error occurred. Please try again later.</p>";
                console.error(xhr.statusText);
            }
        }
    };
    xhr.send(`email=${encodeURIComponent(email)}`);
}
