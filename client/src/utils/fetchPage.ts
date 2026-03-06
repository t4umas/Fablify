import type { BookPage } from "../types";

export async function fetchPage(
  bookId: string,
  page: number,
): Promise<BookPage> {
  const response = await fetch(
    `http://localhost:8000/books/${bookId}/pages/${page}`,
  );

  if (!response.ok)
    throw new Error(`Failed to fetch page ${page} of book ${bookId}`);

  const pageData: BookPage = await response.json();
  return pageData;
}
