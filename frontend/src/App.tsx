import { Input } from './pages/InputPage';
import { ThemeProvider } from "@/components/theme-provider"
import { Recommendations } from './pages/RecommendationsPage';

const App = () => {
  return (
    <ThemeProvider defaultTheme="dark" storageKey="vite-ui-theme">
      <Input />
      <Recommendations />
    </ThemeProvider>
  );
};

export default App;
