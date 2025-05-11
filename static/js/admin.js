// admin.js
document.addEventListener('DOMContentLoaded', function() {
    // Получаем данные из JSON-блока
    const config = JSON.parse(document.getElementById('config-data').textContent);
    let confirmedOffset = config.confirmedOffset;
    let pendingOffset = config.pendingOffset;

    const loadMoreConfirmedBtn = document.getElementById('load-more-confirmed');
    const loadMorePendingBtn = document.getElementById('load-more-pending');

    const confirmedTable = document.getElementById('confirmed-users-table');
    if (confirmedTable) {
        confirmedTable.addEventListener('click', function(e) {
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

    if (loadMoreConfirmedBtn) {
        loadMoreConfirmedBtn.addEventListener('click', function() {
            fetch(`/admin/load_more?section=confirmed&offset=${confirmedOffset}`)
                .then(response => response.ok ? response.json() : Promise.reject('Network error'))
                .then(data => {
                    const table = document.getElementById('confirmed-users-table');
                    if (data && data.users && table) {
                        data.users.forEach(user => {
                            const row = document.createElement('div');
                            row.className = 'list-one statusHealth-sections-table-row';
                            row.innerHTML = `
                                <div>${user.id || ''}</div>
                                <div>${user.username || ''}</div>
                                <div>${user.monopoly_email || 'N/A'}</div>
                                <div><span class="password-mask toggleable" data-password="${user.monopoly_password || 'N/A'}">••••••••</span></div>
                                <div><span class="proxy-mask toggleable" data-proxy="${user.proxy || 'N/A'}">••••••••</span></div>
                                <div class="${user.is_admin ? 'admin-yes' : ''}">${user.is_admin ? 'Да' : 'Нет'}</div>
                                <div>
                                    <form method="POST" action="/admin/delete/${user.id || ''}" style="display:inline;">
                                        <button type="submit" class="button button-small button-grapefruit">Удалить</button>
                                    </form>
                                </div>
                            `;
                            table.appendChild(row);
                        });
                        confirmedOffset += data.users.length;
                        if (!data.has_more) loadMoreConfirmedBtn.style.display = 'none';
                    }
                })
                .catch(error => console.error('Ошибка загрузки подтвержденных пользователей:', error));
        });
    }

    if (loadMorePendingBtn) {
        loadMorePendingBtn.addEventListener('click', function() {
            fetch(`/admin/load_more?section=pending&offset=${pendingOffset}`)
                .then(response => response.ok ? response.json() : Promise.reject('Network error'))
                .then(data => {
                    const table = document.getElementById('pending-users-table');
                    if (data && data.users && table) {
                        data.users.forEach(user => {
                            const row = document.createElement('div');
                            row.className = 'list-one statusHealth-sections-table-row';
                            row.innerHTML = `
                                <div>${user.id || ''}</div>
                                <div>${user.username || ''}</div>
                                <div>
                                    <form method="POST" action="/admin/confirm/${user.id || ''}" style="display:inline;">
                                        <button type="submit" class="button button-small button-grass">Принять</button>
                                    </form>
                                    <form method="POST" action="/admin/delete/${user.id || ''}" style="display:inline;">
                                        <button type="submit" class="button button-small button-grapefruit">Удалить</button>
                                    </form>
                                </div>
                            `;
                            table.appendChild(row);
                        });
                        pendingOffset += data.users.length;
                        if (!data.has_more) loadMorePendingBtn.style.display = 'none';
                    }
                })
                .catch(error => console.error('Ошибка загрузки неподтвержденных пользователей:', error));
        });
    }
});