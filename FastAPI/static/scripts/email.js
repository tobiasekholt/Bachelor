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
    fetch("/send_zip_file", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            email: email
        })
    })
    .then(response => {
        // Display a success message
        document.getElementById("filesPreview").innerHTML = "<p>Email sent successfully!</p>";
    })
    .catch(error => {
        // Display an error message
        document.getElementById("filesPreview").innerHTML = "<p>An error occurred. Please try again later.</p>";
        console.error(error);
    });
}

// Call the getFiles function when the page loads
getFiles();
