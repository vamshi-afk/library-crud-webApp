    async function fetchBooks() {
      const res = await fetch('/books');
      const data = await res.json();
      const tbody = document.getElementById('booksTableBody');
      tbody.innerHTML = '';
      data.forEach(book => {
        tbody.innerHTML += `
          <tr>
            <td>${book.id}</td>
            <td>${book.title}</td>
            <td>${book.author}</td>
            <td>${book.available_copies} / ${book.total_copies}</td>
          </tr>
        `;
      });
    }

    document.getElementById('bookForm').addEventListener('submit', async (e) => {
      e.preventDefault();
      const title = document.getElementById('title').value;
      const author = document.getElementById('author').value;
      const total_copies = parseInt(document.getElementById('copies').value);

      await fetch('/books', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title, author, total_copies })
      });

      document.getElementById('title').value = '';
      document.getElementById('author').value = '';
      document.getElementById('copies').value = '1';
      fetchBooks();
    });

    fetchBooks();

