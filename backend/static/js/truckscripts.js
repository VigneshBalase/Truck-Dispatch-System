document.addEventListener('DOMContentLoaded', function () {
    // Handle form submission for adding new truck details
    document.getElementById('add-truck-form').addEventListener('submit', function (event) {
        event.preventDefault();
        const formData = new FormData(this);
        const data = {};
        formData.forEach((value, key) => {
            data[key] = value;
        });

        fetch('/truck_details', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message);
                location.reload(); // Refresh the page to see new truck details
            } else {
                alert(data.error || 'An error occurred while adding the truck.');
            }
        })
        .catch(error => console.error('Error:', error));
    });

    // Handle form submission for updating truck details
    if (document.getElementById('update-truck-form')) {
        document.getElementById('update-truck-form').addEventListener('submit', function (event) {
            event.preventDefault();
            const formData = new FormData(this);
            const data = {};
            formData.forEach((value, key) => {
                data[key] = value;
            });

            const truckId = data.id; // Assuming the form includes an ID field

            fetch(`/update_truck/${truckId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    alert(data.message);
                    location.reload(); // Refresh the page to see updated truck details
                } else {
                    alert(data.error || 'An error occurred while updating the truck.');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    }

    // Handle deleting truck details
    document.querySelectorAll('.delete-truck-btn').forEach(button => {
        button.addEventListener('click', function () {
            const truckId = this.dataset.truckId;
            fetch(`/delete_truck/${truckId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ id: truckId }),
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    alert(data.message);
                    location.reload(); // Refresh the page to see updated truck details
                } else {
                    alert(data.error || 'An error occurred while deleting the truck.');
                }
            })
            .catch(error => console.error('Error:', error));
        });
    });
});

function editTruck(truckId) {
    window.location.href = `/update_truck/${truckId}`;
}

function deleteTruck(truckId) {
    if (confirm("Are you sure you want to delete this truck?")) {
        fetch(`/delete_truck/${truckId}`, {
            method: 'DELETE',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.message) {
                alert(data.message);
                location.reload(); // Refresh the page to see updated truck list
            } else {
                alert(data.error || 'An error occurred while deleting the truck.');
            }
        })
        .catch(error => console.error('Error:', error));
    }
}
