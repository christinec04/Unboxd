"use client";

import { useState } from "react";
import { InputGroup, InputGroupInput } from "@/components/ui/input-group";
import { useRouter } from "next/navigation";
import { FieldDescription } from "@/components/ui/field"
import { TypeAnimation } from 'react-type-animation';
import { ModeToggle } from '@/components/theme-toggle';
import Wave from 'react-wavify';

export default function HomePage() {
  const description = "Please enter your Letterboxd username, not your display name.";
  const [username, setUsername] = useState("");
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    if (!username) { return; }
    router.push(`/recommendations?username=${username}`);
  };

  return (
    <div className="min-h-screen w-full bg-background flex flex-col">
      
      <div className="flex-1 flex flex-col p-8 z-50">
        {/* Header */}
        <div className="flex justify-end items-center">
          <ModeToggle />
        </div>

        {/* Main Content */}
        <div className="flex-1 flex items-center justify-center">
          <div className="w-full max-w-lg space-y-8">
            <TypeAnimation
              sequence={['Movie Recommendation System']}
              wrapper="span"
              style={{ fontSize: '2em', display: 'inline-block' }}
            />

            <form onSubmit={handleSubmit}>
              <InputGroup className="bg-accent/55 backdrop-blur-md">
                <InputGroupInput id="username"
                  type="text"
                  placeholder="username"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  autoComplete="off" />
              </InputGroup>
            </form>

            <FieldDescription className="ml-2">{description}</FieldDescription>
          </div>
        </div>
      </div>
      
      {/* Wave background */}
      <Wave
        fill="url(#gradient)"
        paused={false}
        style={{
          position: 'absolute',
          bottom: 0,
          left: 0,
          width: '100%',
          zIndex: 0,
        }}
        options={{
          height: 20,
          amplitude: 20,
          speed: 0.15,
          points: 3,
        }}
      >
        <defs>
          <linearGradient id="gradient" gradientTransform="rotate(90)">
            <stop offset="10%"  stopColor="var(--color-blue-300)" />
            <stop offset="90%" stopColor="var(--color-blue-100)" />
          </linearGradient>
        </defs>
      </Wave>

    </div>
  );
}
