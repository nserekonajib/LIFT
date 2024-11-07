document.getElementById('full_name').addEventListener('blur', function() {
    const fullName = this.value;

    // Make an AJAX request to check the full name in the database
    fetch(`/check_name?name=${fullName}`)
        .then(response => response.json())
        .then(data => {
            const nameCheck = document.getElementById('name_check');
            if (data.exists) {
                nameCheck.textContent = "Correct";
                nameCheck.style.color = "green";
            } else {
                nameCheck.textContent = "Not found";
            }
        });
});
