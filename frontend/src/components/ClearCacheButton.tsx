import { useState } from "react";
import { clearCache } from "../services/stockApi";

function ClearCacheButton() {
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");

  async function handleClick() {
    setBusy(true);
    setMessage("");

    try {
      const removed = await clearCache();
      setMessage(
        removed === null
          ? "Cache cleared."
          : `Cleared ${removed} old cache ${removed === 1 ? "entry" : "entries"}.`
      );
    } catch (err) {
      setMessage(err instanceof Error ? err.message : "Failed to clear cache.");
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="clear-cache">
      <button onClick={handleClick} disabled={busy}>
        {busy ? "Clearing..." : "Clear old cache"}
      </button>
      {message && <span>{message}</span>}
    </div>
  );
}

export default ClearCacheButton;