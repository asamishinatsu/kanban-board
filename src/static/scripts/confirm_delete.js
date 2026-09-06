document.addEventListener('DOMContentLoaded', function () {
    const confirmDialog = document.getElementById('confirmDeleteModal');
    const confirmText = document.getElementById('confirmDeleteText');
    const confirmForm = document.getElementById('confirmDeleteForm');

    document.querySelectorAll('form[data-confirm-delete]').forEach(function (form) {
        form.addEventListener('submit', function (event) {
            event.preventDefault();
            confirmText.textContent = form.dataset.confirmDelete || 'Are you sure you want to delete this?';
            confirmForm.action = form.action;
            confirmDialog.showModal();
        });
    });
});