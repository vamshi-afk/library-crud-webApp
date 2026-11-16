// ==================== BOOKS ====================
async function fetchBooks() {
  const res = await fetch('/books/');
  const data = await res.json();

  const tbody = document.getElementById('booksTableBody');
  const bookSelect = document.getElementById('borrowBookSelect');
  tbody.innerHTML = '';
  bookSelect.innerHTML = '<option value="" disabled selected>Choose a book...</option>';

  data.forEach(book => {
    tbody.innerHTML += `
      <tr>
        <td>${book.id}</td>
        <td>${book.title}</td>
        <td>${book.author}</td>
        <td>${book.available_copies} / ${book.total_copies}</td>
        <td>
          <button onclick="deleteBook(${book.id})" class="btn btn-sm btn-danger">Delete</button>
        </td>
      </tr>
    `;

    bookSelect.innerHTML += `
      <option value="${book.id}" ${book.available_copies === 0 ? 'disabled' : ''}>
        #${book.id} - ${book.title} (${book.available_copies} avail)
      </option>
    `;
  });
}

async function deleteBook(id) {
  const res = await fetch(`/books/${id}`, { method: 'DELETE' });
  if (res.ok) {
    await fetchBooks();
  } else {
    const errorData = await res.json();
    alert(`Error: ${errorData.detail}`);
  }
}

document.getElementById('bookForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const title = document.getElementById('title').value;
  const author = document.getElementById('author').value;
  const total_copies = parseInt(document.getElementById('copies').value);

  const res = await fetch('/books/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title, author, total_copies })
  });

  if (res.ok) {
    e.target.reset();
    document.getElementById('copies').value = '1';
    await fetchBooks();
  } else {
    const errorData = await res.json();
    alert(`Error: ${errorData.detail}`);
  }
});

// ==================== MEMBERS ====================
async function fetchMembers() {
  const res = await fetch('/members/');
  const data = await res.json();

  const tbody = document.getElementById('membersTableBody');
  const memberSelect = document.getElementById('borrowMemberSelect');
  tbody.innerHTML = '';
  memberSelect.innerHTML = '<option value="" disabled selected>Choose a member...</option>';

  data.forEach(member => {
    tbody.innerHTML += `
      <tr>
        <td>${member.id}</td>
        <td>${member.name}</td>
        <td>${member.email}</td>
        <td>
          <button onclick="deleteMember(${member.id})" class="btn btn-sm btn-danger">Delete</button>
        </td>
      </tr>
    `;

    memberSelect.innerHTML += `
      <option value="${member.id}">#${member.id} - ${member.name} (${member.email})</option>
    `;
  });
}

async function deleteMember(id) {
  const res = await fetch(`/members/${id}`, { method: 'DELETE' });
  if (res.ok) {
    await fetchMembers();
  } else {
    const errorData = await res.json();
    alert(`Error: ${errorData.detail}`);
  }
}

document.getElementById('memberForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const name = document.getElementById('memberName').value;
  const email = document.getElementById('memberEmail').value;

  const res = await fetch('/members/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ name, email })
  });

  if (res.ok) {
    e.target.reset();
    await fetchMembers();
  } else {
    const errorData = await res.json();
    alert(`Error: ${errorData.detail}`);
  }
});

// ==================== BORROW & LOANS ====================
async function fetchLoans() {
  const res = await fetch('/borrow/');
  const data = await res.json();

  const tbody = document.getElementById('loansTableBody');
  tbody.innerHTML = '';

  data.forEach(record => {
    const borrowedDate = new Date(record.borrowed_at).toLocaleString();
    const actionCell = record.returned_at
      ? `<span class="badge bg-secondary">Returned (${new Date(record.returned_at).toLocaleDateString()})</span>`
      : `<button onclick="returnBook(${record.id})" class="btn btn-sm btn-warning">Return Book</button>`;

    tbody.innerHTML += `
      <tr>
        <td>${record.id}</td>
        <td><strong>${record.book.title}</strong> <small class="text-muted">(#${record.book_id})</small></td>
        <td>${record.member.name} </td>
        <td>${borrowedDate}</td>
        <td>${actionCell}</td>
      </tr>
    `;
  });
}

async function returnBook(recordId) {
  const res = await fetch(`/borrow/return/${recordId}`, { method: 'PUT' });
  if (res.ok) {
    await Promise.all([fetchLoans(), fetchBooks()]);
  } else {
    const errorData = await res.json();
    alert(`Error: ${errorData.detail}`);
  }
}

document.getElementById('borrowForm').addEventListener('submit', async (e) => {
  e.preventDefault();
  const book_id = parseInt(document.getElementById('borrowBookSelect').value);
  const member_id = parseInt(document.getElementById('borrowMemberSelect').value);

  const res = await fetch('/borrow/', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ book_id, member_id })
  });

  if (res.ok) {
    e.target.reset();
    await Promise.all([fetchLoans(), fetchBooks()]);
  } else {
    const errorData = await res.json();
    alert(`Error: ${errorData.detail}`);
  }
});

// ==================== INITIAL LOAD ====================
fetchBooks();
fetchMembers();
fetchLoans();
