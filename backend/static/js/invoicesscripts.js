// document.addEventListener('DOMContentLoaded', () => {
//     const form = document.getElementById('invoiceForm');
//     const invoicesTable = document.getElementById('invoicesTable');

//     form.addEventListener('submit', async (event) => {
//         event.preventDefault(); // Prevent default form submission

//         const formData = new FormData(form);
//         const data = Object.fromEntries(formData.entries());

//         try {
//             const response = await fetch('/invoices', {
//                 method: 'POST',
//                 headers: {
//                     'Content-Type': 'application/json',
//                 },
//                 body: JSON.stringify(data),
//             });

//             if (response.ok) {
//                 alert('Invoice generated successfully!');
//                 form.reset(); // Clear the form
//                 location.reload(); // Reload the page to show the new invoice
//             } else {
//                 const errorData = await response.json();
//                 alert(`Error: ${errorData.error}`);
//             }
//         } catch (error) {
//             console.error('Error:', error);
//             alert('Error generating invoice.');
//         }
//     });

//     invoicesTable.addEventListener('click', async (event) => {
//         if (event.target.classList.contains('delete-btn')) {
//             const invoiceRow = event.target.closest('tr');
//             const invoiceId = invoiceRow.dataset.id;

//             try {
//                 const response = await fetch(`/delete_invoice/${invoiceId}`, {
//                     method: 'DELETE',
//                 });

//                 if (response.ok) {
//                     alert('Invoice deleted successfully!');
//                     invoiceRow.remove(); // Remove the invoice from the DOM
//                 } else {
//                     const errorData = await response.json();
//                     alert(`Error: ${errorData.error}`);
//                 }
//             } catch (error) {
//                 console.error('Error:', error);
//                 alert('Error deleting invoice.');
//             }
//         }

//         if (event.target.classList.contains('update-btn')) {
//             const invoiceRow = event.target.closest('tr');
//             const invoiceId = invoiceRow.dataset.id;
//             const invoiceNumber = prompt('Enter new Invoice Number:', invoiceRow.querySelector('td:nth-child(1)').textContent);
//             const dispatchPlanId = prompt('Enter new Dispatch Plan ID:', invoiceRow.querySelector('td:nth-child(2)').textContent);
//             const amount = prompt('Enter new Amount:', invoiceRow.querySelector('td:nth-child(3)').textContent);

//             if (invoiceNumber && dispatchPlanId && amount) {
//                 try {
//                     const response = await fetch(`/update_invoice/${invoiceId}`, {
//                         method: 'POST',
//                         headers: {
//                             'Content-Type': 'application/json',
//                         },
//                         body: JSON.stringify({ invoice_number: invoiceNumber, dispatch_plan_id: dispatchPlanId, amount: amount }),
//                     });

//                     if (response.ok) {
//                         alert('Invoice updated successfully!');
//                         location.reload(); // Reload the page to show the updated invoice
//                     } else {
//                         const errorData = await response.json();
//                         alert(`Error: ${errorData.error}`);
//                     }
//                 } catch (error) {
//                     console.error('Error:', error);
//                     alert('Error updating invoice.');
//                 }
//             } else {
//                 alert('All fields are required for updating.');
//             }
//         }
//     });
// });










document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('invoiceForm');
    const invoicesTable = document.getElementById('invoicesTable');

    form.addEventListener('submit', async (event) => {
        event.preventDefault(); // Prevent default form submission

        const formData = new FormData(form);
        const data = Object.fromEntries(formData.entries());

        try {
            const response = await fetch('/invoices', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data),
            });

            if (response.ok) {
                alert('Invoice generated successfully!');
                form.reset(); // Clear the form
                location.reload(); // Reload the page to show the new invoice
            } else {
                const errorData = await response.json();
                alert(`Error: ${errorData.error}`);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Error generating invoice.');
        }
    });

    invoicesTable.addEventListener('click', async (event) => {
        if (event.target.classList.contains('delete-btn')) {
            const invoiceRow = event.target.closest('tr');
            const invoiceId = invoiceRow.dataset.id;

            try {
                const response = await fetch(`/delete_invoice/${invoiceId}`, {
                    method: 'DELETE',
                });

                if (response.ok) {
                    alert('Invoice deleted successfully!');
                    invoiceRow.remove(); // Remove the invoice from the DOM
                } else {
                    const errorData = await response.json();
                    alert(`Error: ${errorData.error}`);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('Error deleting invoice.');
            }
        }

        if (event.target.classList.contains('update-btn')) {
            const invoiceRow = event.target.closest('tr');
            const invoiceId = invoiceRow.dataset.id;

            // Redirect to the update_invoice route with the invoice ID
            window.location.href = `/update_invoice/${invoiceId}`;
        }
    });
});
