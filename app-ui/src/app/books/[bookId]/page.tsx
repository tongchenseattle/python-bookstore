import Link from "next/link";
import { notFound } from "next/navigation";

import { apiGet } from "../../../lib/api-client";

type BookDetailPageProps = {
  params: { bookId: string };
};

type StorefrontBookDetail = {
  id: string;
  title: string;
  description: string | null;
  price: number;
  publish_date: string;
  status: string;
};

export default async function BookDetailPage({ params }: BookDetailPageProps) {
  let book: StorefrontBookDetail;

  try {
    book = await apiGet<StorefrontBookDetail>(
      `/catalog/books/${params.bookId}`,
    );
  } catch (error) {
    const status = (error as { status?: number }).status;
    if (status === 404) {
      notFound();
    }
    return (
      <main style={{ padding: "2rem", maxWidth: "720px", margin: "0 auto" }}>
        <h1>Book Detail</h1>
        <p>Unable to load this book right now. Please try again.</p>
        <p>
          <Link href="/">Back to store</Link>
        </p>
      </main>
    );
  }

  const addToCartHref = `/cart?add=${book.id}&title=${encodeURIComponent(book.title)}&price=${book.price.toFixed(2)}`;

  return (
    <main style={{ padding: "2rem", maxWidth: "720px", margin: "0 auto" }}>
      <p>
        <Link href="/">Back to store</Link>
      </p>
      <h1>{book.title}</h1>
      <p>
        <strong>Price:</strong> ${book.price.toFixed(2)}
      </p>
      <p>
        <strong>Published:</strong> {book.publish_date}
      </p>
      <p>
        <strong>Status:</strong> {book.status}
      </p>
      <p>{book.description ?? "No description available."}</p>
      <p>
        <Link href={addToCartHref}>Buy this book</Link>
      </p>
    </main>
  );
}
