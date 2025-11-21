import { useState } from "react";
import {
  InputGroup,
  InputGroupAddon,
  InputGroupInput,
} from "@/components/ui/input-group"
import { ModeToggle } from "@/components/theme-toggle"
import api from '../app/api';
import { Button } from "@/components/ui/button";

const navItems = [
  { href: "/", label: "Home" },
  { href: "https://github.iu.edu/B365-Fall2025/Project-ez2-ermili-cch8-dvchavan", label: "Docs", isExternal: true },
]

export function NavBar(){
  const [username, setUsername] = useState("");

  // Submit username to backend
  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();

    if (!username) { return;}

    try { 
      let response = await api.post('/username', { username: username });
      console.log(response.data.message);

      if (response.data.status === false) {
        throw new Error(response.data.message);
      }

      response = await api.get(`/recommendations/${username}`);
      console.log(response);
    } 
    catch (error) {
      console.error(error);
      return;
    }
  };

  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background-55 backdrop-blur-sm">
      <div className="container mx-auto p-4 sm:px-6 lg:px-8 flex gap-2 justify-between">
        <div className="flex flex-wrap gap-2">
          { /* Navigation Items */ }
          <div>
            {navItems.map((item) => (
              <Button variant="link" onClick={() => window.open(item.href, "_self")}>{item.label}</Button>
            ))}
          </div>

          { /* Username Input */ }
          <form className="sm:w-sm" onSubmit={handleSubmit}>
            <InputGroup>
              <InputGroupInput id="username"
              type="text"
              placeholder="username"
              value={username}                
              onChange={(e) => setUsername(e.target.value)} 
              autoComplete="off"/>
            </InputGroup>
          </form>
          </div>

          { /* Theme Toggle */ }
          <ModeToggle />
          
        </div>
    </header>
  )
}