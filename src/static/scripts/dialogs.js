document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('[data-dialog-target]').forEach(function (trigger) {
        trigger.addEventListener('click', function () {
            const dialog = document.getElementById(trigger.dataset.dialogTarget);
            if (dialog) dialog.showModal();
        });
    });

    document.querySelectorAll('[data-dialog-close]').forEach(function (closeBtn) {
        closeBtn.addEventListener('click', function () {
            const dialog = closeBtn.closest('dialog');
            if (dialog) dialog.close();
        });
    });
});