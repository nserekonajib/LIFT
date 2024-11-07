document.addEventListener("DOMContentLoaded", function () {
    const userId = "{{ session['user_id'] }}"; // Fetch user_id from session
    const subscription = "{{ subscription_plan }}"; // Fetch subscription plan from backend
    const requiredAmount = "{{ required_amount }}"; // Fetch required amount

    // Show the appropriate popup based on subscription status
    if (!subscription) {
        if (subscription) {
            // Show the investment plans popup
            document.getElementById('modal').style.display = 'none';
            document.getElementById('plans-popup').style.display = 'block';
        } else {
            // Show the welcome modal if no subscription exists
            displayModal();
        }
    }

    // Function to show the modal popup
    function displayModal() {
        document.getElementById('modal').style.display = 'block';

        // Event listener for the close button
        document.getElementById('btn-close-modal').addEventListener('click', hideModal);
    }

    // Function to close the modal popup
    function hideModal() {
        document.getElementById('modal').style.display = 'none';
    }
});

// Function to close the investment plans popup
function closePopup() {
    document.getElementById('plans-popup').style.display = 'none';
}

// Function to redirect to deposit page when subscribing to a plan
function subscribe(plan) {
    const requiredAmount = {
        'starter': 30,  // Amount for starter plan
        'bronze': 99,   // Amount for bronze plan
        'gold': 500     // Amount for gold plan
    };

    // Redirect to the deposit page with the required amount based on the selected plan
    // window.location.href = `/subscribe/<plan>?amount=${requiredAmount[plan]}`;
}

