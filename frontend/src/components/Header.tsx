interface HeaderProps {
  darkMode: boolean;
  onToggle: () => void;
}

function Header({ darkMode, onToggle }: HeaderProps) {
  return (
    <header className="header">
      <h1>Stock Analysis</h1>

      <button onClick={onToggle} className="theme-button">
        {darkMode ? "☀ Light mode" : "☾ Dark mode"}
      </button>
    </header>
  );
}

export default Header;
