
import { useEffect, useState } from "react";

export default function BackendStatus() {
  const [status, setStatus] = useState("Checking...");

  useEffect(() => {
    fetch("/api/health")
      .then((response) => {
        if (!response.ok) {
          throw new Error("Backend returned an error");
        }

        return response.json();
      })
      .then((data) => {
        setStatus(
          data.status === "ok"
            ? "Connected"
            : "Unexpected response"
        );
      })
      .catch((error) => {
        console.error("Backend connection failed:", error);
        setStatus("Disconnected");
      });
  }, []);

  return (
    <div className="backend-status">
      Python backend: {status}
    </div>
  );
}
