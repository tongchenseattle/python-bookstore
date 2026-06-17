import { isAuthenticated } from "../../lib/auth";

export default function CheckoutPage() {
  if (!isAuthenticated()) {
    return (
      <main>
        <h1>Sign in required</h1>
        <p>Please sign in to continue checkout.</p>
      </main>
    );
  }

  return (
    <main>
      <h1>Checkout</h1>
    </main>
  );
}
