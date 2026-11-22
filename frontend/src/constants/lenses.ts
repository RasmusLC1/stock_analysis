export const LENSES = [
  "Average",
  "Growth",
  "Value",
  "Health",
  "Quality",
  "Garp",
  "Scale Disruptor",
] as const;

export type Lens = (typeof LENSES)[number];
