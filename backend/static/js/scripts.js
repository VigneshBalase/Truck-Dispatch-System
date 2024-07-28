document.getElementById('dispatchForm').addEventListener('submit', function(event) {
    event.preventDefault();

    const formData = {
        source: document.getElementById('source').value,
        source_id: document.getElementById('source_id').value,
        destination: document.getElementById('destination').value,
        destination_id: document.getElementById('destination_id').value,
        product_code: document.getElementById('product_code').value,
        product_description: document.getElementById('product_description').value,
        priority: document.getElementById('priority').value,
        qty_case: document.getElementById('qty_case').value,
        weight_tons: document.getElementById('weight_tons').value,
        truck_type_required: document.getElementById('truck_type_required').value
    };

    if (!formData.source || !formData.source_id || !formData.destination || !formData.destination_id || !formData.product_code || !formData.product_description) {
        alert('Please fill in all required fields.');
        return;
    }

    console.log('Submitting form data:', formData);

    fetch('/dispatch_plans', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => {
        console.log('POST response:', response);
        if (!response.ok) {
            throw new Error('Network response was not ok.');
        }
        return response.json();
    })
    .then(data => {
        console.log('POST success:', data);
        fetchDispatchPlans(); // Fetch and display the updated list
        document.getElementById('dispatchForm').reset(); // Reset form after submission
        alert('Dispatch plan added successfully!');
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('Failed to add dispatch plan. Please try again.');
    });
});

function fetchDispatchPlans() {
    console.log('Fetching dispatch plans...');
    fetch('/dispatch_plans')
        .then(response => {
            console.log('GET response:', response);
            if (!response.ok) {
                throw new Error('Network response was not ok.');
            }
            return response.json();
        })
        .then(data => {
            console.log('Fetched dispatch plans:', data); // Debugging
            const tableBody = document.querySelector('#dispatchTable tbody');
            tableBody.innerHTML = ''; // Clear existing table data
            data.forEach(plan => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${plan.id}</td>
                    <td>${plan.source}</td>
                    <td>${plan.source_id}</td>
                    <td>${plan.destination}</td>
                    <td>${plan.destination_id}</td>
                    <td>${plan.product_code}</td>
                    <td>${plan.product_description}</td>
                    <td>${plan.priority}</td>
                    <td>${plan.qty_case}</td>
                    <td>${plan.weight_tons}</td>
                    <td>${plan.truck_type_required}</td>
                    <td>
                        <button onclick="editDispatchPlan(${plan.id})">Edit</button>
                        <button onclick="deleteDispatchPlan(${plan.id})">Delete</button>
                    </td>
                `;
                tableBody.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error fetching dispatch plans:', error);
            alert('Failed to fetch dispatch plans. Please try again.');
        });
}

function editDispatchPlan(id) {
    console.log('Editing dispatch plan ID:', id);
    window.location.href = `/update/${id}`;
}

function deleteDispatchPlan(id) {
    console.log('Deleting dispatch plan ID:', id);
    fetch(`/dispatch_plans/${id}`, {
        method: 'DELETE'
    })
    .then(response => {
        console.log('DELETE response:', response);
        if (!response.ok) {
            throw new Error('Network response was not ok.');
        }
        return response.json();
    })
    .then(data => {
        console.log('Deleted:', data);
        fetchDispatchPlans(); // Fetch and display the updated list
        alert('Dispatch plan deleted successfully!');
    })
    .catch((error) => {
        console.error('Error:', error);
        alert('Failed to delete dispatch plan. Please try again.');
    });
}

document.addEventListener('DOMContentLoaded', fetchDispatchPlans);
