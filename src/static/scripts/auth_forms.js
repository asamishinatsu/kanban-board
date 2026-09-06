document.addEventListener('DOMContentLoaded', function () {
    document.querySelectorAll('form[data-ajax-form]').forEach(function (form) {
        const errorEl = form.querySelector('[data-form-error]');

        form.addEventListener('submit', function (event) {
            event.preventDefault();

            errorEl.hidden = true;

            fetch(form.action, {
                method: 'POST',
                body: new FormData(form)
            })
                .then(function (response) {
                    return response.json().then(function (data) {
                        return { ok: response.ok, data: data };
                    });
                })
                .then(function (result) {
                    if (result.ok && result.data.success) {
                        window.location.reload();
                    } else {
                        errorEl.textContent = result.data.error || 'Something went wrong';
                        errorEl.hidden = false;
                    }
                })
                .catch(function () {
                    errorEl.textContent = 'Network error, try again';
                    errorEl.hidden = false;
                });
        });
    });
});