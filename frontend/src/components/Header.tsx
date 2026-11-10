
interface HeaderProps {
  darkMode: boolean;
  onToggleTheme: () => void;
}

export default function Header({
  darkMode,
  onToggleTheme,
}: HeaderProps) {
  return (
    <header className="header">
      <div className="brand">
        <div className="brand-icon">S</div>
        <h1>Stock Analysis</h1>
      </div>

      <button
        className="theme-button"
        onClick={onToggleTheme}
      >
        {darkMode ? "☀ Light mode" : "☾ Dark mode"}
      </button>
    </header>
  );
}
