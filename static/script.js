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

function deleteItem(itemId) {
    if (confirm('Are you sure you want to delete this item? This action cannot be undone.')) {
        // Add loading state
        const deleteButton = document.querySelector(`[onclick="deleteItem(${itemId})"]`);
        const originalContent = deleteButton.innerHTML;
        deleteButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
        deleteButton.disabled = true;
        
        fetch(`/delete_item/${itemId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Remove the item from the DOM with a smooth animation
                const itemElement = document.querySelector(`[data-item-id="${itemId}"]`);
                if (itemElement) {
                    itemElement.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
                    itemElement.style.opacity = '0';
                    itemElement.style.transform = 'translateX(-20px)';
                    setTimeout(() => {
                        itemElement.remove();
                        // Check if this was the last item
                        const itemsList = document.querySelector('.items-list');
                        const remainingItems = itemsList.querySelectorAll('.item');
                        if (remainingItems.length === 0) {
                            itemsList.innerHTML = `
                                <p class="no-items">
                                    <i class="fas fa-inbox"></i>
                                    No items in this checklist. Add your first item!
                                </p>
                            `;
                        }
                    }, 300);
                }
            } else {
                // Restore button state on failure
                deleteButton.innerHTML = originalContent;
                deleteButton.disabled = false;
                alert('Failed to delete item. Please try again.');
            }
        })
        .catch(error => {
            // Restore button state on error
            deleteButton.innerHTML = originalContent;
            deleteButton.disabled = false;
            console.error('Error:', error);
            alert('Failed to delete item. Please try again.');
        });
    }
}

function deleteChecklist(checklistId) {
    if (confirm('Are you sure you want to delete this entire checklist? This will also delete all items in it and cannot be undone.')) {
        // Add loading state to button
        const deleteButton = document.querySelector(`[onclick="deleteChecklist(${checklistId})"]`);
        if (deleteButton) {
            const originalContent = deleteButton.innerHTML;
            deleteButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Deleting...';
            deleteButton.disabled = true;
        }
        
        fetch(`/delete_checklist/${checklistId}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Show success message and redirect
                if (window.location.pathname.includes('/checklist/')) {
                    // If we're on the checklist page, redirect to dashboard
                    window.location.href = '/dashboard';
                } else {
                    // If we're on dashboard, remove the card with animation
                    const checklistCard = deleteButton.closest('.checklist-card');
                    if (checklistCard) {
                        checklistCard.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
                        checklistCard.style.opacity = '0';
                        checklistCard.style.transform = 'scale(0.95)';
                        setTimeout(() => {
                            checklistCard.remove();
                            // Check if this was the last checklist
                            const checklistsGrid = document.querySelector('.checklists-grid');
                            const remainingChecklists = checklistsGrid.querySelectorAll('.checklist-card');
                            if (remainingChecklists.length === 0) {
                                checklistsGrid.innerHTML = `
                                    <p class="no-checklists">
                                        <i class="fas fa-clipboard"></i>
                                        No checklists yet. Create your first one!
                                    </p>
                                `;
                            }
                        }, 300);
                    }
                }
            } else {
                // Restore button state on failure
                if (deleteButton) {
                    deleteButton.innerHTML = originalContent;
                    deleteButton.disabled = false;
                }
                alert('Failed to delete checklist. Please try again.');
            }
        })
        .catch(error => {
            // Restore button state on error  
            if (deleteButton) {
                deleteButton.innerHTML = originalContent;
                deleteButton.disabled = false;
            }
            console.error('Error:', error);
            alert('Failed to delete checklist. Please try again.');
        });
    }
} 