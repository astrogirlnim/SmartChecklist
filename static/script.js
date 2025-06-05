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
            const item = document.querySelector(`input[onchange="toggleItem(${itemId})"]`).closest('.item, .subitem');
            item.classList.toggle('checked');
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert('Failed to update item status. Please try again.');
    });
}

function deleteItem(itemId) {
    if (confirm('Are you sure you want to delete this item? This will also delete any sub-items and cannot be undone.')) {
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
                const itemElement = document.querySelector(`[data-item-id="${itemId}"]`).closest('.item-container, .subitem');
                if (itemElement) {
                    itemElement.style.transition = 'opacity 0.3s ease, transform 0.3s ease';
                    itemElement.style.opacity = '0';
                    itemElement.style.transform = 'translateX(-20px)';
                    setTimeout(() => {
                        itemElement.remove();
                        // Check if this was the last item
                        const itemsList = document.querySelector('.items-list');
                        const remainingItems = itemsList.querySelectorAll('.item-container');
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

function showEditForm(itemId, content, url) {
    console.log('showEditForm called with:', itemId, content, url);
    console.log('URL type:', typeof url, 'URL value:', JSON.stringify(url));
    
    // Hide all other edit forms first
    document.querySelectorAll('.edit-item-form').forEach(form => {
        form.style.display = 'none';
    });
    
    // Show the edit form for this item
    const editForm = document.getElementById(`edit-form-${itemId}`);
    const contentInput = document.getElementById(`edit-content-${itemId}`);
    const urlInput = document.getElementById(`edit-url-${itemId}`);
    
    console.log('Found elements:', { editForm: !!editForm, contentInput: !!contentInput, urlInput: !!urlInput });
    
    if (editForm && contentInput && urlInput) {
        // Set values carefully
        const cleanContent = content || '';
        const cleanUrl = url || '';
        
        console.log('Setting values - Content:', JSON.stringify(cleanContent), 'URL:', JSON.stringify(cleanUrl));
        
        contentInput.value = cleanContent;
        urlInput.value = cleanUrl;
        
        console.log('Values after setting - Content:', JSON.stringify(contentInput.value), 'URL:', JSON.stringify(urlInput.value));
        
        editForm.style.display = 'block';
        
        // Force URL input to be interactive and clear any interference
        urlInput.style.pointerEvents = 'auto';
        urlInput.style.position = 'relative';
        urlInput.style.zIndex = '10';
        urlInput.disabled = false;
        urlInput.readOnly = false;
        urlInput.style.opacity = '1';
        urlInput.style.cursor = 'text';
        
        // Remove any existing event listeners and add new ones
        urlInput.replaceWith(urlInput.cloneNode(true));
        const newUrlInput = document.getElementById(`edit-url-${itemId}`);
        newUrlInput.value = cleanUrl;
        
        // Add debugging event listeners
        newUrlInput.addEventListener('click', function(e) {
            console.log('URL input clicked!');
            e.stopPropagation();
            newUrlInput.focus();
        });
        
        newUrlInput.addEventListener('focus', function() {
            console.log('URL input focused!');
        });
        
        newUrlInput.addEventListener('blur', function() {
            console.log('URL input blurred!');
        });
        
        newUrlInput.addEventListener('input', function() {
            console.log('URL input changed:', newUrlInput.value);
        });
        
        newUrlInput.addEventListener('keydown', function(e) {
            console.log('URL input keydown:', e.key);
        });
        
        // Test click immediately
        setTimeout(() => {
            console.log('URL input properties after timeout:');
            console.log('  disabled:', newUrlInput.disabled);
            console.log('  readOnly:', newUrlInput.readOnly);
            console.log('  value:', JSON.stringify(newUrlInput.value));
            console.log('  style.pointerEvents:', newUrlInput.style.pointerEvents);
            console.log('  offsetWidth:', newUrlInput.offsetWidth);
            console.log('  offsetHeight:', newUrlInput.offsetHeight);
        }, 100);
        
        contentInput.focus();
        console.log('Edit form shown successfully');
    } else {
        console.error('Could not find required elements for edit form');
    }
}

function cancelEditItem(itemId) {
    const editForm = document.getElementById(`edit-form-${itemId}`);
    if (editForm) {
        editForm.style.display = 'none';
    }
}

function saveEditItem(itemId) {
    const contentInput = document.getElementById(`edit-content-${itemId}`);
    const urlInput = document.getElementById(`edit-url-${itemId}`);
    
    console.log('saveEditItem called for item:', itemId);
    console.log('Found inputs:', { contentInput: !!contentInput, urlInput: !!urlInput });
    
    if (!contentInput || !urlInput) {
        alert('Edit form not found');
        return;
    }
    
    const content = contentInput.value.trim();
    const url = urlInput.value.trim();
    
    console.log('Saving values - Content:', JSON.stringify(content), 'URL:', JSON.stringify(url));
    
    if (!content) {
        alert('Content is required');
        contentInput.focus();
        return;
    }
    
    // Show loading state
    const saveButton = document.querySelector(`[onclick="saveEditItem(${itemId})"]`);
    const originalContent = saveButton.innerHTML;
    saveButton.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Saving...';
    saveButton.disabled = true;
    
    const formData = new FormData();
    formData.append('content', content);
    formData.append('url', url);
    
    fetch(`/edit_item/${itemId}`, {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Update the item display
            const itemTextElement = document.querySelector(`[data-item-id="${itemId}"] .item-text`);
            const itemLinkElement = document.querySelector(`[data-item-id="${itemId}"] .item-link`);
            
            if (itemTextElement) {
                itemTextElement.textContent = content;
            }
            
            // Handle link display
            if (url) {
                if (itemLinkElement) {
                    itemLinkElement.href = url;
                } else {
                    // Create new link element
                    const itemContent = document.querySelector(`[data-item-id="${itemId}"] .item-content`);
                    const linkElement = document.createElement('a');
                    linkElement.href = url;
                    linkElement.target = '_blank';
                    linkElement.className = 'item-link';
                    linkElement.title = 'Open link';
                    linkElement.innerHTML = '<i class="fas fa-external-link-alt"></i>';
                    itemContent.appendChild(linkElement);
                }
            } else if (itemLinkElement) {
                // Remove link if URL was cleared
                itemLinkElement.remove();
            }
            
            // Hide edit form
            cancelEditItem(itemId);
        } else {
            alert(data.error || 'Failed to update item. Please try again.');
        }
        
        // Restore button state
        saveButton.innerHTML = originalContent;
        saveButton.disabled = false;
    })
    .catch(error => {
        // Restore button state on error
        saveButton.innerHTML = originalContent;
        saveButton.disabled = false;
        console.error('Error:', error);
        alert('Failed to update item. Please try again.');
    });
}

function showSubitemForm(itemId) {
    // Hide all other subitem forms first
    document.querySelectorAll('.add-subitem-form').forEach(form => {
        form.style.display = 'none';
    });
    
    // Show the subitem form for this item
    const subitemForm = document.getElementById(`subitem-form-${itemId}`);
    if (subitemForm) {
        subitemForm.style.display = 'block';
        const contentInput = subitemForm.querySelector('input[name="content"]');
        if (contentInput) {
            contentInput.focus();
        }
    }
}

function hideSubitemForm(itemId) {
    const subitemForm = document.getElementById(`subitem-form-${itemId}`);
    if (subitemForm) {
        subitemForm.style.display = 'none';
        // Clear the form
        const inputs = subitemForm.querySelectorAll('input[type="text"], input[type="url"]');
        inputs.forEach(input => input.value = '');
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