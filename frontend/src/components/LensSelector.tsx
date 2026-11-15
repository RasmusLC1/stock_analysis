interface LensSelectorProps {
  lenses: readonly string[];
  active: string;
  onChange: (lens: string) => void;
}

function LensSelector({ lenses, active, onChange }: LensSelectorProps) {
  return (
    <div className="lens-selector">
      <label htmlFor="lens-select">Active Lens:</label>

      <select
        id="lens-select"
        value={active}
        onChange={(event) => onChange(event.target.value)}
      >
        {lenses.map((lens) => (
          <option key={lens} value={lens}>
            {lens}
          </option>
        ))}
      </select>
    </div>
  );
}

export default LensSelector;
