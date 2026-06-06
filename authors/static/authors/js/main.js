document.addEventListener('DOMContentLoaded', () => {

    // ============================================================
    // 1. DARK / LIGHT THEME TOGGLE
    // ============================================================
    const themeBtn = document.getElementById('theme-toggle-btn');
    const moonIcon = themeBtn ? themeBtn.querySelector('.theme-icon-moon') : null;
    const sunIcon  = themeBtn ? themeBtn.querySelector('.theme-icon-sun')  : null;

    function applyTheme(dark) {
        if (dark) {
            document.body.classList.add('dark-theme');
            if (moonIcon) moonIcon.style.display = 'none';
            if (sunIcon)  sunIcon.style.display  = '';
        } else {
            document.body.classList.remove('dark-theme');
            if (moonIcon) moonIcon.style.display = '';
            if (sunIcon)  sunIcon.style.display  = 'none';
        }
    }

    // Restore saved preference
    const savedTheme = localStorage.getItem('psicogram_theme');
    applyTheme(savedTheme === 'dark');

    if (themeBtn) {
        themeBtn.addEventListener('click', () => {
            const isDark = document.body.classList.contains('dark-theme');
            applyTheme(!isDark);
            localStorage.setItem('psicogram_theme', isDark ? 'light' : 'dark');
        });
    }

    // ============================================================
    // 2. SEARCH DRAWER
    // ============================================================
    const searchNavBtn  = document.getElementById('search-nav-btn');
    const searchDrawer  = document.getElementById('search-drawer');
    const searchInput   = document.getElementById('search-input');
    const clearSearchBtn = document.getElementById('clear-search-btn');
    const searchItems   = document.querySelectorAll('.search-result-item');
    let drawerOpen = false;

    function openDrawer() {
        if (!searchDrawer) return;
        drawerOpen = true;
        searchDrawer.classList.add('open');
        if (searchInput) setTimeout(() => searchInput.focus(), 300);
        if (searchNavBtn) searchNavBtn.classList.add('active');
    }

    function closeDrawer() {
        if (!searchDrawer) return;
        drawerOpen = false;
        searchDrawer.classList.remove('open');
        if (searchNavBtn) searchNavBtn.classList.remove('active');
        if (searchInput) { searchInput.value = ''; filterSearch(''); }
    }

    if (searchNavBtn) {
        searchNavBtn.addEventListener('click', () => {
            drawerOpen ? closeDrawer() : openDrawer();
        });
    }

    // Close drawer on click outside
    document.addEventListener('click', (e) => {
        if (drawerOpen && searchDrawer && !searchDrawer.contains(e.target) && !searchNavBtn.contains(e.target)) {
            closeDrawer();
        }
    });

    // Real-time filtering
    function filterSearch(query) {
        const q = query.toLowerCase().trim();
        searchItems.forEach(item => {
            const name     = item.dataset.name     || '';
            const username = item.dataset.username || '';
            const match = name.includes(q) || username.includes(q);
            item.classList.toggle('hidden', !match);
        });
        if (clearSearchBtn) clearSearchBtn.classList.toggle('visible', q.length > 0);
    }

    if (searchInput) {
        searchInput.addEventListener('input', () => filterSearch(searchInput.value));
    }
    if (clearSearchBtn) {
        clearSearchBtn.addEventListener('click', () => {
            if (searchInput) searchInput.value = '';
            filterSearch('');
            if (searchInput) searchInput.focus();
        });
    }

    // ============================================================
    // 3. ACTIVE USER SELECTION POPUP
    // ============================================================
    let currentUser = { username: 'visitante', name: 'Visitante Académico', pfp: '/static/img/default_avatar.png' };
    const storedUser = localStorage.getItem('psicogram_user');
    if (storedUser) { try { currentUser = JSON.parse(storedUser); } catch(e) {} }
    updateActiveUserUI();

    const userTrigger = document.getElementById('active-user-trigger');
    const userPopup   = document.getElementById('user-menu-popup');

    if (userTrigger && userPopup) {
        userTrigger.addEventListener('click', (e) => {
            e.stopPropagation();
            userPopup.classList.toggle('show');
        });
        document.addEventListener('click', () => userPopup.classList.remove('show'));

        document.querySelectorAll('.user-menu-item').forEach(item => {
            item.addEventListener('click', () => {
                currentUser = { username: item.dataset.username, name: item.dataset.name, pfp: item.dataset.pfp };
                localStorage.setItem('psicogram_user', JSON.stringify(currentUser));
                updateActiveUserUI();
                userPopup.classList.remove('show');
            });
        });
    }

    function updateActiveUserUI() {
        const sidebarPfp  = document.querySelector('.active-user-avatar');
        const sidebarName = document.querySelector('.active-user-name');
        const sidebarRole = document.querySelector('.active-user-role');
        if (sidebarPfp)  sidebarPfp.src = currentUser.pfp;
        if (sidebarName) sidebarName.textContent = currentUser.name;
        if (sidebarRole) sidebarRole.textContent = currentUser.username === 'visitante' ? 'Visitante' : `@${currentUser.username}`;

        const suggPfp  = document.querySelector('.user-suggestion-pfp');
        const suggUser = document.querySelector('.user-suggestion-username');
        const suggName = document.querySelector('.user-suggestion-fullname');
        if (suggPfp)  suggPfp.src = currentUser.pfp;
        if (suggUser) suggUser.textContent = currentUser.username;
        if (suggName) suggName.textContent = currentUser.name;
    }

    // ============================================================
    // 4. MODAL CORE (Close Logic)
    // ============================================================
    const postModal     = document.getElementById('post-detail-modal');
    const academicModal = document.getElementById('academic-info-modal');

    document.querySelectorAll('.modal-close-btn').forEach(btn => btn.addEventListener('click', closeAllModals));
    document.querySelectorAll('.modal-overlay').forEach(overlay => {
        overlay.addEventListener('click', (e) => { if (e.target === overlay) closeAllModals(); });
    });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeAllModals(); });

    function closeAllModals() {
        if (postModal)     postModal.style.display     = 'none';
        if (academicModal) academicModal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }

    // ============================================================
    // 5. ACADEMIC MODAL
    // ============================================================
    const openAcademicBtn = document.getElementById('open-academic-btn');
    if (openAcademicBtn && academicModal) {
        openAcademicBtn.addEventListener('click', () => {
            academicModal.style.display = 'flex';
            document.body.style.overflow = 'hidden';
        });
    }

    // ============================================================
    // 6. POST DETAIL MODAL (AJAX)
    // ============================================================
    document.querySelectorAll('.grid-post-card').forEach(card => {
        card.addEventListener('click', () => openPostDetail(card.dataset.postId));
    });
    document.querySelectorAll('.view-comments-btn').forEach(btn => {
        btn.addEventListener('click', () => openPostDetail(btn.dataset.postId));
    });

    function openPostDetail(postId) {
        if (!postModal) return;
        const modalImg       = document.getElementById('modal-post-img');
        const modalAuthorPfp = document.getElementById('modal-author-pfp');
        const modalAuthorUser = document.getElementById('modal-author-username');
        const modalAuthorLoc = document.getElementById('modal-author-location');
        const modalComments  = document.getElementById('modal-comments-list');
        const modalLikes     = document.getElementById('modal-likes-count');
        const modalTime      = document.getElementById('modal-post-time');
        const modalPostId    = document.getElementById('modal-comment-post-id');

        if (modalImg) modalImg.src = '';
        if (modalComments) modalComments.innerHTML = '<div style="text-align:center;padding:30px;color:var(--text-secondary);">Cargando...</div>';

        postModal.style.display = 'flex';
        document.body.style.overflow = 'hidden';

        fetch(`/api/post/${postId}/`)
            .then(r => r.json())
            .then(data => {
                if (modalImg)       modalImg.src = data.image_url;
                if (modalAuthorPfp) modalAuthorPfp.src = data.author_pfp;
                if (modalAuthorUser) { modalAuthorUser.textContent = data.author_username; modalAuthorUser.href = `/p/${data.author_username}/`; }
                if (modalAuthorLoc) modalAuthorLoc.textContent = data.location || data.author_occupation;
                if (modalLikes)     modalLikes.textContent = `${Number(data.likes_count).toLocaleString('es-ES')} Me gusta`;
                if (modalTime)      modalTime.textContent = data.created_at;
                if (modalPostId)    modalPostId.value = data.id;

                if (modalComments) {
                    modalComments.innerHTML = `
                        <div class="modal-caption-item">
                            <img src="${data.author_pfp}" alt="" class="modal-comment-pfp">
                            <div class="modal-comment-text-box">
                                <div><span class="modal-comment-author">${data.author_username}</span>${data.caption}</div>
                                <div class="modal-comment-time">${data.created_at}</div>
                            </div>
                        </div>`;
                    (data.comments || []).forEach(c => {
                        modalComments.innerHTML += `
                            <div class="modal-comment-item">
                                <img src="${c.pfp_url}" alt="" class="modal-comment-pfp">
                                <div class="modal-comment-text-box">
                                    <div><span class="modal-comment-author">${c.author_name}</span>${c.text}</div>
                                    <div class="modal-comment-time">${c.created_at}</div>
                                </div>
                            </div>`;
                    });
                }
            })
            .catch(() => { if (modalComments) modalComments.innerHTML = '<div style="color:red;padding:20px;text-align:center;">Error al cargar.</div>'; });
    }

    // ============================================================
    // 7. LIKE BUTTONS (All)
    // ============================================================
    document.querySelectorAll('.like-btn').forEach(btn => {
        btn.addEventListener('click', () => toggleLike(btn));
    });

    function toggleLike(btn) {
        btn.classList.toggle('liked');
        const container = btn.closest('.post-card, .post-modal-actions');
        const likesEl   = container ? container.querySelector('.post-likes, .post-modal-likes') : null;
        if (likesEl) {
            const match = likesEl.textContent.replace(/\./g, '').match(/\d+/);
            if (match) {
                let n = parseInt(match[0]);
                n = btn.classList.contains('liked') ? n + 1 : n - 1;
                likesEl.textContent = `${n.toLocaleString('es-ES')} Me gusta`;
            }
        }
        const svg = btn.querySelector('svg');
        if (svg) {
            svg.style.transform = 'scale(1.4)';
            svg.style.transition = 'transform 0.15s cubic-bezier(0.17,0.89,0.32,1.28)';
            setTimeout(() => { svg.style.transform = 'scale(1)'; }, 200);
        }
    }

    // ============================================================
    // 8. DOUBLE-CLICK HEART ANIMATION on Post Images
    // ============================================================
    document.querySelectorAll('.post-image-container').forEach(container => {
        let lastTap = 0;
        container.addEventListener('dblclick', (e) => doHeartPop(container, e));
        // Mobile double-tap support
        container.addEventListener('touchend', (e) => {
            const now = Date.now();
            if (now - lastTap < 350) {
                doHeartPop(container, e.changedTouches[0]);
            }
            lastTap = now;
        });
    });

    function doHeartPop(container, e) {
        // Auto-like the post
        const card    = container.closest('.post-card');
        const likeBtn = card ? card.querySelector('.like-btn') : null;
        if (likeBtn && !likeBtn.classList.contains('liked')) toggleLike(likeBtn);

        // Remove any existing heart
        const old = container.querySelector('.heart-pop');
        if (old) old.remove();

        const heart = document.createElement('div');
        heart.className = 'heart-pop';
        heart.innerHTML = `<svg viewBox="0 0 24 24"><path d="M12 21.35l-1.45-1.32C5.4 15.36 2 12.28 2 8.5 2 5.42 4.42 3 7.5 3c1.74 0 3.41.81 4.5 2.09C13.09 3.81 14.76 3 16.5 3 19.58 3 22 5.42 22 8.5c0 3.78-3.4 6.86-8.55 11.54L12 21.35z"/></svg>`;
        container.appendChild(heart);
        setTimeout(() => heart.remove(), 750);
    }

    // ============================================================
    // 9. FOLLOW BUTTON (Profile Page)
    // ============================================================
    const followBtn = document.getElementById('profile-follow-btn');
    const followersCount = document.querySelector('.profile-stat-item:nth-child(2) .profile-stat-value');

    if (followBtn) {
        followBtn.addEventListener('click', () => {
            const isFollowing = followBtn.classList.contains('following');
            if (isFollowing) {
                // Unfollow
                followBtn.classList.remove('following');
                followBtn.textContent = 'Seguir';
                followBtn.style.backgroundColor = '';
                followBtn.style.color = '';
                if (followersCount) {
                    let n = parseInt(followersCount.textContent.replace(/\./g, '').replace(/,/g, '')) || 0;
                    followersCount.textContent = (n - 1).toLocaleString('es-ES');
                }
            } else {
                // Follow
                followBtn.classList.add('following');
                followBtn.textContent = '✔ Siguiendo';
                followBtn.style.backgroundColor = '';
                followBtn.style.color = '';
                if (followersCount) {
                    let n = parseInt(followersCount.textContent.replace(/\./g, '').replace(/,/g, '')) || 0;
                    followersCount.textContent = (n + 1).toLocaleString('es-ES');
                }
                // Small animation
                followBtn.style.transform = 'scale(0.95)';
                setTimeout(() => followBtn.style.transform = '', 150);
            }
        });
    }

    // ============================================================
    // 10. FEED COMMENT FORMS (AJAX)
    // ============================================================
    document.querySelectorAll('.comment-input-form').forEach(form => {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const input  = form.querySelector('.comment-input');
            const postId = form.dataset.postId;
            const text   = input.value.trim();
            if (!text) return;
            submitComment(postId, text, (comment) => {
                input.value = '';
                const previewList = document.getElementById(`comments-preview-${postId}`);
                if (previewList) {
                    const item = document.createElement('div');
                    item.className = 'comment-preview-item';
                    item.innerHTML = `<span class="comment-preview-user">${comment.author_name}</span> ${comment.text}`;
                    previewList.appendChild(item);
                }
                const countBtn = form.closest('.post-card').querySelector('.view-comments-btn');
                if (countBtn) {
                    const m = countBtn.textContent.match(/\d+/);
                    const n = m ? parseInt(m[0]) + 1 : 1;
                    countBtn.textContent = `Ver los ${n} comentarios`;
                }
            });
        });
    });

    // ============================================================
    // 11. MODAL COMMENT FORM (AJAX)
    // ============================================================
    const modalCommentForm = document.getElementById('modal-comment-form');
    if (modalCommentForm) {
        modalCommentForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const input  = document.getElementById('modal-comment-input');
            const postId = document.getElementById('modal-comment-post-id').value;
            const text   = input.value.trim();
            if (!text) return;
            submitComment(postId, text, (comment) => {
                input.value = '';
                const area = document.getElementById('modal-comments-list');
                if (area) {
                    area.innerHTML += `
                        <div class="modal-comment-item">
                            <img src="${comment.pfp_url}" alt="" class="modal-comment-pfp">
                            <div class="modal-comment-text-box">
                                <div><span class="modal-comment-author">${comment.author_name}</span>${comment.text}</div>
                                <div class="modal-comment-time">${comment.created_at}</div>
                            </div>
                        </div>`;
                    area.scrollTop = area.scrollHeight;
                }
                const previewList = document.getElementById(`comments-preview-${postId}`);
                if (previewList) {
                    const item = document.createElement('div');
                    item.className = 'comment-preview-item';
                    item.innerHTML = `<span class="comment-preview-user">${comment.author_name}</span> ${comment.text}`;
                    previewList.appendChild(item);
                }
            });
        });
    }

    // ============================================================
    // 12. SHARED SUBMIT COMMENT UTIL
    // ============================================================
    function submitComment(postId, text, callback) {
        fetch('/api/comment/add/', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ post_id: postId, author_name: currentUser.username, text })
        })
        .then(r => { if (!r.ok) throw new Error(); return r.json(); })
        .then(data => { if (data.success) callback(data.comment); })
        .catch(() => alert('Error al enviar el comentario.'));
    }

    // ============================================================
    // 13. FEED PAGE: Sugerencias "Cambiar" button wires to user popup
    // ============================================================
    const suggSwitch = document.getElementById('sugg-switch');
    if (suggSwitch) {
        suggSwitch.addEventListener('click', () => {
            const trigger = document.getElementById('active-user-trigger');
            if (trigger) trigger.click();
        });
    }
});
