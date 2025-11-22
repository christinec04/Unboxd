"use client";

import { useState } from "react";
import { InputGroup, InputGroupInput, InputGroupAddon } from "@/components/ui/input-group";
import { Spinner } from "@/components/ui/spinner";
import { useRouter } from "next/navigation";
import { FieldDescription } from "@/components/ui/field"
import { TypeAnimation } from 'react-type-animation';
import api from "@/app/api/index";

export default function HomePage() {
  const description = "Please enter your Letterboxd username, not your display name.";
  const [username, setUsername] = useState("");
  const [loading, setLoading] = useState(false);
  const router = useRouter();
  const [errorMessage, setErrorMessage] = useState(description);

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!username) { return; }

    setLoading(true);
    setErrorMessage(description);

    try {
      await api.post('/usernames/', { username: username });
    }
    catch (error) {
      console.error(error);
      setLoading(false);
      setErrorMessage("Error: " + (error instanceof Error ? error.message : "Unknown error"));
      return;
    }

    // Navigate to next page
    router.push(`/recommendations?username=${username}`);
  };

  return (
    <div className="@container grid h-screen place-items-center">
      <div className="w-full max-w-md flex flex-col gap-5">

        <TypeAnimation
          sequence={['Movie Recommendation System']}
          wrapper="span"
          style={{ fontSize: '2em', display: 'inline-block' }}
        />

        <form onSubmit={handleSubmit}>
          <InputGroup>
            <InputGroupInput id="username"
              type="text"
              placeholder="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              autoComplete="off" />

            <InputGroupAddon align="inline-end">
              {loading && <Spinner />}
            </InputGroupAddon>
          </InputGroup>
        </form>

        <FieldDescription className="ml-2">{errorMessage}</FieldDescription>
      </div>
    </div>
  );
}
