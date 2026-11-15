interface HeaderProps {
  darkMode: boolean;
  onToggle: () => void;
}

function Header({ darkMode, onToggle }: HeaderProps) {
  return (
    <header className="header">
      <h1>Stock Analysis</h1>

    </header>
  );
}

export default Header;
