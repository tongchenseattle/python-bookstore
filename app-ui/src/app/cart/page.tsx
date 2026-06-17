"use client";

import Link from "next/link";
import { useEffect, useMemo, useRef, useState } from "react";
import { useSearchParams } from "next/navigation";

const CART_STORAGE_KEY = "bookstore_cart_v1";

type CartItem = {
  bookId: string;
  title: string;
  price: number;
  quantity: number;
};

function readCartFromStorage(): CartItem[] {
  const raw = window.localStorage.getItem(CART_STORAGE_KEY);
  if (!raw) {
    return [];
  }

  try {
    const parsed = JSON.parse(raw) as CartItem[];
    if (!Array.isArray(parsed)) {
      return [];
    }
    return parsed.filter(
      (item) =>
        !!item.bookId &&
        !!item.title &&
        Number.isFinite(item.price) &&
        Number.isFinite(item.quantity) &&
        item.quantity > 0,
    );
  } catch {
    return [];
  }
}

function saveCartToStorage(items: CartItem[]): void {
  window.localStorage.setItem(CART_STORAGE_KEY, JSON.stringify(items));
}

export default function CartPage() {
  const searchParams = useSearchParams();
  const [items, setItems] = useState<CartItem[]>([]);
  const [message, setMessage] = useState("");
  const hasLoadedCart = useRef(false);
  const lastProcessedAddKey = useRef<string>("");

  useEffect(() => {
    const stored = readCartFromStorage();
    setItems(stored);
    hasLoadedCart.current = true;
  }, []);

  useEffect(() => {
    if (!hasLoadedCart.current) {
      return;
    }

    const addBookId = searchParams.get("add");
    const title = searchParams.get("title");
    const rawPrice = searchParams.get("price");

    if (!addBookId || !title || !rawPrice) {
      return;
    }

    const dedupeKey = `${addBookId}:${title}:${rawPrice}`;
    if (lastProcessedAddKey.current === dedupeKey) {
      return;
    }

    const price = Number.parseFloat(rawPrice);
    if (!Number.isFinite(price) || price < 0) {
      setMessage("Unable to add book to cart due to invalid price.");
      return;
    }

    setItems((previous) => {
      const existing = previous.find((item) => item.bookId === addBookId);
      let updated: CartItem[];

      if (existing) {
        updated = previous.map((item) =>
          item.bookId === addBookId
            ? { ...item, quantity: item.quantity + 1 }
            : item,
        );
      } else {
        updated = [
          ...previous,
          {
            bookId: addBookId,
            title,
            price,
            quantity: 1,
          },
        ];
      }

      saveCartToStorage(updated);
      return updated;
    });

    lastProcessedAddKey.current = dedupeKey;
    setMessage(`Added "${title}" to cart.`);
    window.history.replaceState({}, "", "/cart");
  }, [searchParams]);

  const subtotal = useMemo(() => {
    return items.reduce((acc, item) => acc + item.price * item.quantity, 0);
  }, [items]);

  function updateQuantity(bookId: string, nextQuantity: number): void {
    const normalized = Math.max(1, nextQuantity);
    setItems((previous) => {
      const updated = previous.map((item) =>
        item.bookId === bookId ? { ...item, quantity: normalized } : item,
      );
      saveCartToStorage(updated);
      return updated;
    });
  }

  function removeItem(bookId: string): void {
    setItems((previous) => {
      const updated = previous.filter((item) => item.bookId !== bookId);
      saveCartToStorage(updated);
      return updated;
    });
  }

  return (
    <main style={{ padding: "2rem", maxWidth: "960px", margin: "0 auto" }}>
      <h1>Your Cart</h1>

      <p>
        <Link href="/">Continue shopping</Link>
      </p>

      {message ? <p>{message}</p> : null}

      {items.length === 0 ? (
        <p>Your cart is empty.</p>
      ) : (
        <>
          <ul
            style={{
              listStyle: "none",
              padding: 0,
              display: "grid",
              gap: "0.75rem",
            }}
          >
            {items.map((item) => {
              const lineTotal = item.price * item.quantity;
              return (
                <li
                  key={item.bookId}
                  style={{
                    border: "1px solid #ddd",
                    borderRadius: "8px",
                    padding: "0.75rem 1rem",
                    display: "grid",
                    gap: "0.5rem",
                  }}
                >
                  <div
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      gap: "1rem",
                    }}
                  >
                    <strong>{item.title}</strong>
                    <span>${lineTotal.toFixed(2)}</span>
                  </div>

                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: "0.5rem",
                    }}
                  >
                    <button
                      type="button"
                      onClick={() =>
                        updateQuantity(item.bookId, item.quantity - 1)
                      }
                    >
                      -
                    </button>
                    <span>Qty: {item.quantity}</span>
                    <button
                      type="button"
                      onClick={() =>
                        updateQuantity(item.bookId, item.quantity + 1)
                      }
                    >
                      +
                    </button>
                    <span style={{ marginLeft: "0.5rem", color: "#444" }}>
                      ${item.price.toFixed(2)} each
                    </span>
                    <button
                      type="button"
                      style={{ marginLeft: "auto" }}
                      onClick={() => removeItem(item.bookId)}
                    >
                      Remove
                    </button>
                  </div>
                </li>
              );
            })}
          </ul>

          <p style={{ marginTop: "1rem", fontWeight: 700 }}>
            Subtotal: ${subtotal.toFixed(2)}
          </p>
          <p>
            <Link href="/checkout">Proceed to checkout</Link>
          </p>
        </>
      )}
    </main>
  );
}
