type AdminCatalogFormProps = {
  mode: "category" | "book";
};

export function AdminCatalogForm({ mode }: AdminCatalogFormProps) {
  return (
    <form>
      <h2>{mode === "category" ? "Category" : "Book"} Form</h2>
      <button type="submit">Save</button>
    </form>
  );
}
