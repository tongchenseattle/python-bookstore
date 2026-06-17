type BookDetailPageProps = {
  params: { bookId: string };
};

export default function BookDetailPage({ params }: BookDetailPageProps) {
  return (
    <main>
      <h1>Book Detail</h1>
      <p>Book ID: {params.bookId}</p>
    </main>
  );
}
