// profile.js
document.addEventListener('DOMContentLoaded', function() {
    const profileTable = document.getElementById('profile-account-table');
    if (profileTable) {
        profileTable.addEventListener('click', function(e) {
            const target = e.target;
            if (target && target.classList.contains('toggleable')) {
                e.preventDefault();
                const isPassword = target.classList.contains('password-mask');
                const dataAttr = isPassword ? 'data-password' : 'data-proxy';
                const originalValue = target.getAttribute(dataAttr) || 'N/A';
                target.textContent = target.textContent === '••••••••' ? originalValue : '••••••••';
            }
        });
    }
});