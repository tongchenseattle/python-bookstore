import Link from "next/link";

import { apiGet } from "../lib/api-client";

const PAGE_SIZE = 10;

type HomePageProps = {
  searchParams?: {
    page?: string;
  };
};

type StorefrontBook = {
  id: string;
  title: string;
  price: number;
  status: string;
};

function parsePage(rawPage: string | undefined): number {
  const parsed = Number.parseInt(rawPage ?? "1", 10);
  if (!Number.isFinite(parsed) || parsed < 1) {
    return 1;
  }
  return parsed;
}

export default async function HomePage({ searchParams }: HomePageProps) {
  const currentPage = parsePage(searchParams?.page);

  let allBooks: StorefrontBook[] = [];
  let loadError = "";

  try {
    allBooks = await apiGet<StorefrontBook[]>("/catalog/books");
  } catch {
    loadError = "Unable to load books right now. Please try again.";
  }

  const totalBooks = allBooks.length;
  const totalPages = Math.max(1, Math.ceil(totalBooks / PAGE_SIZE));
  const page = Math.min(currentPage, totalPages);
  const start = (page - 1) * PAGE_SIZE;
  const books = allBooks.slice(start, start + PAGE_SIZE);

  const previousPage = page > 1 ? page - 1 : null;
  const nextPage = page < totalPages ? page + 1 : null;

  return (
    <main style={{ padding: "2rem", maxWidth: "960px", margin: "0 auto" }}>
      <h1>Bookstore</h1>
      <p>Browse books and pick one to buy. Showing 10 books per page.</p>

      {loadError ? <p>{loadError}</p> : null}

      {!loadError && books.length === 0 ? <p>No books available.</p> : null}

      {!loadError ? (
        <>
          <ul
            style={{
              listStyle: "none",
              padding: 0,
              display: "grid",
              gap: "0.75rem",
            }}
          >
            {books.map((book) => (
              <li
                key={book.id}
                style={{
                  border: "1px solid #ddd",
                  borderRadius: "8px",
                  padding: "0.75rem 1rem",
                  display: "flex",
                  justifyContent: "space-between",
                  alignItems: "center",
                  gap: "1rem",
                }}
              >
                <div>
                  <h2 style={{ margin: 0, fontSize: "1rem" }}>{book.title}</h2>
                  <p style={{ margin: "0.25rem 0 0", color: "#444" }}>
                    ${book.price.toFixed(2)} | {book.status}
                  </p>
                </div>
                <Link href={`/books/${book.id}`}>View & Buy</Link>
              </li>
            ))}
          </ul>

          <nav
            aria-label="Pagination"
            style={{
              display: "flex",
              justifyContent: "space-between",
              marginTop: "1rem",
            }}
          >
            {previousPage ? (
              <Link href={`/?page=${previousPage}`}>Previous</Link>
            ) : (
              <span />
            )}
            <span>
              Page {page} of {totalPages} ({totalBooks} books)
            </span>
            {nextPage ? (
              <Link href={`/?page=${nextPage}`}>Next</Link>
            ) : (
              <span />
            )}
          </nav>
        </>
      ) : null}
    </main>
  );
}
