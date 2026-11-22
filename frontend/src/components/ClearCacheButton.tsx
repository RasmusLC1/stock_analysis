import { useState } from "react";
import { clearCache } from "../services/stockApi";

function ClearCacheButton() {
  const [busy, setBusy] = useState(false);
  const [result, setResult] = useState<{ text: string; isError: boolean } | null>(null);

  async function handleClick() {
    setBusy(true);
    setResult(null);

    try {
      const removed = await clearCache();
      setResult({
        text:
          removed === null
            ? "Cache cleared"
            : `Cleared ${removed} old ${removed === 1 ? "entry" : "entries"}`,
        isError: false,
      });
    } catch (err) {
      setResult({
        text: err instanceof Error ? err.message : "Failed to clear cache",
        isError: true,
      });
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="clear-cache">
      <button onClick={handleClick} disabled={busy}>
        {busy ? "Clearing..." : "Clear old cache"}
      </button>

      {result && (
        <span className={result.isError ? "clear-cache-message error" : "clear-cache-message"}>
          {result.text}
        </span>
      )}
    </div>
  );
}

export default ClearCacheButton;