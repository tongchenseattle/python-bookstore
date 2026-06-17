"use client";

import Link from "next/link";
import { useEffect, useRef, useState } from "react";
import { useSearchParams } from "next/navigation";

const APP_API_BASE_URL =
  process.env.NEXT_PUBLIC_APP_API_BASE_URL ?? "http://localhost:8000";
const CART_ID_STORAGE_KEY = "bookstore_cart_id_v1";

type CartItem = {
  book_id: string;
  title: string;
  price: number;
  quantity: number;
  line_total: number;
};

type CartResponse = {
  cart_id: string;
  items: CartItem[];
  subtotal: number;
};

async function apiRequest<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${APP_API_BASE_URL}${path}`, {
    ...init,
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }

  if (response.status === 204) {
    return {} as T;
  }

  return (await response.json()) as T;
}

export default function CartPage() {
  const searchParams = useSearchParams();
  const [cartId, setCartId] = useState("");
  const [items, setItems] = useState<CartItem[]>([]);
  const [subtotal, setSubtotal] = useState(0);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);
  const lastProcessedAddKey = useRef("");

  async function loadCart(nextCartId: string): Promise<void> {
    const cart = await apiRequest<CartResponse>(`/cart/${nextCartId}`, {
      method: "GET",
    });
    setItems(cart.items ?? []);
    setSubtotal(Number(cart.subtotal ?? 0));
  }

  useEffect(() => {
    const existingCartId = window.localStorage.getItem(CART_ID_STORAGE_KEY);
    const nextCartId = existingCartId ?? crypto.randomUUID();
    if (!existingCartId) {
      window.localStorage.setItem(CART_ID_STORAGE_KEY, nextCartId);
    }

    const initializeCart = async () => {
      try {
        await apiRequest(`/cart/${nextCartId}/ensure`, {
          method: "POST",
          body: JSON.stringify({ session_id: "browser-session" }),
        });
        setCartId(nextCartId);
        await loadCart(nextCartId);
      } catch {
        setMessage("Unable to load cart right now. Please try again.");
      } finally {
        setLoading(false);
      }
    };

    void initializeCart();
  }, []);

  useEffect(() => {
    if (!cartId) {
      return;
    }

    const addBookId = searchParams.get("add");
    if (!addBookId) {
      return;
    }

    const dedupeKey = `${cartId}:${addBookId}`;
    if (lastProcessedAddKey.current === dedupeKey) {
      return;
    }

    const addToCart = async () => {
      try {
        await apiRequest("/cart/items", {
          method: "POST",
          body: JSON.stringify({
            cart_id: cartId,
            book_id: addBookId,
            quantity: 1,
          }),
        });
        await loadCart(cartId);
        setMessage("Book added to cart.");
        lastProcessedAddKey.current = dedupeKey;
        window.history.replaceState({}, "", "/cart");
      } catch {
        setMessage("Unable to add this book to cart.");
      }
    };

    void addToCart();
  }, [searchParams, cartId]);

  async function updateQuantity(
    bookId: string,
    nextQuantity: number,
  ): Promise<void> {
    const normalized = Math.max(1, nextQuantity);
    if (!cartId) {
      return;
    }

    try {
      await apiRequest(`/cart/${cartId}/items/${bookId}`, {
        method: "PUT",
        body: JSON.stringify({ quantity: normalized }),
      });
      await loadCart(cartId);
    } catch {
      setMessage("Unable to update cart quantity.");
    }
  }

  async function removeItem(bookId: string): Promise<void> {
    if (!cartId) {
      return;
    }

    try {
      await apiRequest(`/cart/${cartId}/items/${bookId}`, { method: "DELETE" });
      await loadCart(cartId);
    } catch {
      setMessage("Unable to remove item from cart.");
    }
  }

  return (
    <main style={{ padding: "2rem", maxWidth: "960px", margin: "0 auto" }}>
      <h1>Your Cart</h1>

      <p>
        <Link href="/">Continue shopping</Link>
      </p>

      {message ? <p>{message}</p> : null}

      {loading ? <p>Loading cart...</p> : null}

      {!loading && items.length === 0 ? (
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
                    <span>${Number(lineTotal).toFixed(2)}</span>
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
                        void updateQuantity(item.book_id, item.quantity - 1)
                      }
                    >
                      -
                    </button>
                    <span>Qty: {item.quantity}</span>
                    <button
                      type="button"
                      onClick={() =>
                        void updateQuantity(item.book_id, item.quantity + 1)
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
                      onClick={() => void removeItem(item.book_id)}
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
