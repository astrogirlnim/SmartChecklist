function toggleItem(itemId) {
    fetch(`/toggle_item/${itemId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const item = document.querySelector(`input[onchange="toggleItem(${itemId})"]`).closest('.item');
            item.classList.toggle('checked');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to update item status. Please try again.');
    });
} 