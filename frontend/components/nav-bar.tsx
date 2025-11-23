import { useState } from "react";
import {
  InputGroup,
  InputGroupAddon,
  InputGroupInput,
} from "@/components/ui/input-group"
import { ModeToggle } from "@/components/theme-toggle"
import { Button } from "@/components/ui/button";

const navItems = [
  { href: "/", label: "Home" },
  { href: "https://github.iu.edu/B365-Fall2025/Project-ez2-ermili-cch8-dvchavan", label: "Docs", isExternal: true },
]

export function NavBar({ username, setUsername, handleSubmit }){
  return (
    <header className="sticky top-0 z-50 w-full border-b bg-background/55 backdrop-blur-md">
      <div className="container mx-auto p-4 sm:px-6 lg:px-8 flex justify-between gap-4">
        <div className="flex flex-wrap gap-y-4">
          { /* Navigation Links */ }
          {navItems.map((item) => (
            <Button key={item.href} variant="link" onClick={() => window.open(item.href, "_self")}>{item.label}</Button>
          ))}

          { /* Username Input */ }
          <form onSubmit={handleSubmit} className="flex-1 min-w-sm pl-4">
            <InputGroup className="bg-accent/55 backdrop-blur-md">
              <InputGroupInput 
                className="w-full"
                id="username"
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