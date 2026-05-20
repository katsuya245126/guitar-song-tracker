const songList = document.getElementById('song-list');
const searchInput = document.getElementById('search-input');
const songModal = document.getElementById('song-modal');
const importModal = document.getElementById('import-modal');
const songForm = document.getElementById('song-form');
const modalTitle = document.getElementById('modal-title');
const toast = document.getElementById('toast');

let editingIndex = null;
let pendingImport = null;
let toastTimer = null;
let activeFilter = 'all';
let activeTuning = '';
let activeCapo = '';

const tuningFilter = document.getElementById('tuning-filter');
const capoFilter = document.getElementById('capo-filter');

const STATUS_LABELS = {
    'wishlist': 'Wishlist',
    'in-progress': 'In Progress',
    'learned': 'Learned',
};

// ── Utilities ────────────────────────────────────────────────────────────────

function showToast(msg) {
    toast.textContent = msg;
    toast.classList.add('show');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.remove('show'), 3000);
}

function openModal(overlay) {
    overlay.classList.add('open');
}

function closeModal(overlay) {
    overlay.classList.remove('open');
}

// ── Song list ────────────────────────────────────────────────────────────────

async function loadSongs(query = '') {
    const url = query ? `/api/songs?q=${encodeURIComponent(query)}` : '/api/songs';
    const res = await fetch(url);
    let songs = await res.json();
    if (activeFilter !== 'all') {
        songs = songs.filter(s => (s.status || 'wishlist') === activeFilter);
    }
    if (activeTuning) {
        songs = songs.filter(s => s.tuning.toLowerCase() === activeTuning.toLowerCase());
    }
    if (activeCapo !== '') {
        songs = songs.filter(s => String(s.capo) === activeCapo);
    }
    renderSongs(songs);
    updateFilterOptions();
}

function updateFilterOptions() {
    fetch('/api/songs').then(r => r.json()).then(all => {
        const currentTuning = tuningFilter.value;
        const tunings = [...new Set(all.map(s => s.tuning.toUpperCase()))].sort();
        tuningFilter.innerHTML = '<option value="">All tunings</option>' +
            tunings.map(t => `<option value="${t}"${t === currentTuning.toUpperCase() ? ' selected' : ''}>${t}</option>`).join('');

        const currentCapo = capoFilter.value;
        const capos = [...new Set(all.map(s => s.capo))].sort((a, b) => a - b);
        capoFilter.innerHTML = '<option value="">All capos</option>' +
            capos.map(c => `<option value="${c}"${String(c) === currentCapo ? ' selected' : ''}>Capo ${c}</option>`).join('');
    });
}

function renderSongs(songs) {
    songList.innerHTML = '';

    if (!songs.length) {
        songList.innerHTML = '<p class="empty-state">No songs yet. Add one!</p>';
        return;
    }

    songs.forEach((song, i) => {
        const card = document.createElement('div');
        card.className = 'song-card';
        const status = song.status || 'wishlist';
        card.innerHTML = `
            <div class="song-info">
                <h3><a class="song-title-link" href="/song/${i}">${escHtml(song.title)}</a></h3>
                <div class="song-meta">
                    <span>🎸 ${escHtml(song.tuning)}</span>
                    <span>🎵 Capo ${song.capo}</span>
                    <span class="status-badge status-${status}">${STATUS_LABELS[status] || status}</span>
                </div>
            </div>
            <div class="song-actions">
                <button class="btn btn-ghost btn-sm" onclick="openEdit(${i})">Edit</button>
                <button class="btn btn-danger btn-sm" onclick="deleteSong(${i})">Delete</button>
            </div>
        `;
        songList.appendChild(card);
    });
}

function escHtml(str) {
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;');
}

// ── Filter tabs ──────────────────────────────────────────────────────────────

document.querySelectorAll('.filter-tab').forEach(tab => {
    tab.addEventListener('click', () => {
        document.querySelectorAll('.filter-tab').forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
        activeFilter = tab.dataset.status;
        loadSongs(searchInput.value.trim());
    });
});

tuningFilter.addEventListener('change', () => {
    activeTuning = tuningFilter.value;
    loadSongs(searchInput.value.trim());
});

capoFilter.addEventListener('change', () => {
    activeCapo = capoFilter.value;
    loadSongs(searchInput.value.trim());
});

// ── Search ───────────────────────────────────────────────────────────────────

let searchTimer = null;
searchInput.addEventListener('input', () => {
    clearTimeout(searchTimer);
    searchTimer = setTimeout(() => loadSongs(searchInput.value.trim()), 250);
});

document.getElementById('search-btn').addEventListener('click', () => {
    loadSongs(searchInput.value.trim());
});

// ── Add / Edit modal ─────────────────────────────────────────────────────────

document.getElementById('add-btn').addEventListener('click', () => {
    editingIndex = null;
    modalTitle.textContent = 'Add Song';
    songForm.reset();
    openModal(songModal);
});

async function openEdit(index) {
    const res = await fetch('/api/songs');
    const songs = await res.json();
    const song = songs[index];
    if (!song) return;

    editingIndex = index;
    modalTitle.textContent = 'Edit Song';
    document.getElementById('field-title').value = song.title;
    document.getElementById('field-link').value = song.link;
    document.getElementById('field-tuning').value = song.tuning;
    document.getElementById('field-capo').value = song.capo;
    document.getElementById('field-status').value = song.status || 'wishlist';
    openModal(songModal);
}

songForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const payload = {
        title: document.getElementById('field-title').value.trim(),
        link: document.getElementById('field-link').value.trim(),
        tuning: document.getElementById('field-tuning').value.trim(),
        capo: parseInt(document.getElementById('field-capo').value, 10),
        status: document.getElementById('field-status').value,
    };

    const url = editingIndex !== null ? `/api/songs/${editingIndex}` : '/api/songs';
    const method = editingIndex !== null ? 'PUT' : 'POST';

    const res = await fetch(url, {
        method,
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
    });

    if (res.ok) {
        closeModal(songModal);
        loadSongs(searchInput.value.trim());
        showToast(editingIndex !== null ? 'Song updated.' : 'Song added.');
    } else {
        showToast('Something went wrong.');
    }
});

document.getElementById('modal-cancel').addEventListener('click', () => closeModal(songModal));
songModal.addEventListener('click', (e) => { if (e.target === songModal) closeModal(songModal); });

// ── Delete ───────────────────────────────────────────────────────────────────

async function deleteSong(index) {
    if (!confirm('Delete this song?')) return;
    const res = await fetch(`/api/songs/${index}`, { method: 'DELETE' });
    if (res.ok) {
        loadSongs(searchInput.value.trim());
        showToast('Song deleted.');
    } else {
        showToast('Something went wrong.');
    }
}

// ── Export ───────────────────────────────────────────────────────────────────

document.getElementById('export-btn').addEventListener('click', () => {
    window.location.href = '/api/export';
});

// ── Import ───────────────────────────────────────────────────────────────────

document.getElementById('import-btn').addEventListener('click', () => {
    document.getElementById('import-file').value = '';
    document.getElementById('conflict-section').style.display = 'none';
    pendingImport = null;
    openModal(importModal);
});

document.getElementById('import-cancel').addEventListener('click', () => closeModal(importModal));
importModal.addEventListener('click', (e) => { if (e.target === importModal) closeModal(importModal); });

document.getElementById('import-upload-btn').addEventListener('click', async () => {
    const fileInput = document.getElementById('import-file');
    if (!fileInput.files.length) {
        showToast('Please choose a file.');
        return;
    }

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    const res = await fetch('/api/import', { method: 'POST', body: formData });
    const data = await res.json();

    if (!res.ok) {
        showToast(data.error || 'Invalid file.');
        return;
    }

    pendingImport = data;

    if (data.duplicates.length === 0) {
        // No conflicts — confirm immediately
        await confirmImport(false);
        return;
    }

    // Show conflict UI
    const conflictSection = document.getElementById('conflict-section');
    const conflictList = document.getElementById('conflict-list');
    conflictList.innerHTML = data.duplicates.map(s => `<li>${escHtml(s.title)}</li>`).join('');
    conflictSection.style.display = 'block';
});

document.getElementById('import-skip-btn').addEventListener('click', () => confirmImport(false));
document.getElementById('import-overwrite-btn').addEventListener('click', () => confirmImport(true));

async function confirmImport(overwrite) {
    if (!pendingImport) return;

    const res = await fetch('/api/import/confirm', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            new: pendingImport.new,
            duplicates: pendingImport.duplicates,
            overwrite,
        }),
    });

    const data = await res.json();
    if (res.ok) {
        closeModal(importModal);
        loadSongs();
        const msg = `Imported ${data.added} new song(s). ${data.duplicates_handled} duplicate(s) ${overwrite ? 'overwritten' : 'skipped'}.`;
        showToast(msg);
    } else {
        showToast('Import failed.');
    }
}

// ── Init ─────────────────────────────────────────────────────────────────────

loadSongs();
