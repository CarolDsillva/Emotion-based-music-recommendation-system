import { TextEncoder, TextDecoder } from "util";
Object.assign(global, { TextEncoder, TextDecoder }); // needed by react-router v7 in Jest

const { render, screen } = require("@testing-library/react");
const App = require("./App").default;

test("renders the landing page", () => {
  render(<App />);
  expect(screen.getByText(/Discover Music/i)).toBeInTheDocument();
  expect(screen.getByRole("button", { name: /Detect Emotion/i })).toBeInTheDocument();
});

test("shows the subscribe link and developed-by watermark", () => {
  render(<App />);
  const subscribe = screen.getByRole("link", { name: /Subscribe to my channel/i });
  expect(subscribe).toHaveAttribute("href", "https://www.youtube.com/@CarolDsillva?sub_confirmation=1");
  expect(subscribe).toHaveAttribute("target", "_blank");
  expect(screen.getByText(/Developed by Carol Dsilva/i)).toBeInTheDocument();
});
