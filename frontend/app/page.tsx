"use client";

import { useState } from "react";
import { InputGroup, InputGroupInput, InputGroupAddon } from "@/components/ui/input-group";
import { Spinner } from "@/components/ui/spinner";
import { useRouter } from "next/navigation";
import { FieldDescription } from "@/components/ui/field"
import { TypeAnimation } from 'react-type-animation';
import { ModeToggle } from '@/components/theme-toggle';
import { useTheme } from "next-themes";
import { Status } from "@/app/api/types.gen";
import Wave from 'react-wavify';
import api from "@/app/api";

export default function HomePage() {
  type Undefinable<Status> = Status | undefined;

  const description = "Please enter your Letterboxd username, not your display name.";
  const [username, setUsername] = useState("");
  const [status, setStatus] = useState<Undefinable<Status>>(undefined);
  const router = useRouter();
  const [message, setMessage] = useState<Undefinable<string>>(description);

  const getStatus = async (intervalId: NodeJS.Timeout) => {
    const failed: Undefinable<Status>[] = [Status.FAILED_INVALID_USERNAME, 
      Status.FAILED_NO_RATINGS_AND_REVIEWS_TO_SCRAPE_FOR_THE_USER,
      Status.FAILED_ERROR_WHILE_SCRAPING,
      Status.FAILED_NO_DATA_AVAILABLE_ABOUT_THE_USER_RATED_AND_REVIEWS_MOVIES,
      Status.FAILED_NO_TRENDING_MOVIES_NOT_ALREADY_REVIEWED_ARE_AVAILABLE_FOR_RECOMMENDATION];

    try {
      const response = await api.get('/status/', { params: { username } });
      const newStatus = response.data;
      setStatus(newStatus);
      setMessage(newStatus);

      if (status == Status.FINISHED) {
        console.log("Finished");
        clearInterval(intervalId);
        router.push(`/recommendations?username=${username}`);
      }

      if (failed.includes(newStatus)){
        clearInterval(intervalId);
        setMessage("Error: " + newStatus);
        setStatus(undefined);
      } 
    }
    catch (error) {
      clearInterval(intervalId);
      setStatus(undefined);
      setMessage("Error: " + (error instanceof Error ? error.message : "Unknown error"));
    }
  };

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!username) { return; }

    setMessage(description); // reset error message if any
    setStatus(Status.STARTING);

    try {
      await api.post('/usernames/', { username: username });
      const intervalId = setInterval(() => getStatus(intervalId), 2000);
    }
    catch (error) {
      setStatus(undefined);
      setMessage("Error: " + (error instanceof Error ? error.message : "Unknown error"));
      return;
    }
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

                <InputGroupAddon align="inline-end">
                  {(status !== Status.FINISHED 
                  && status !== undefined) 
                  && <Spinner />}
                </InputGroupAddon>
              </InputGroup>
            </form>

            <FieldDescription className="ml-2">{message}</FieldDescription>
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
