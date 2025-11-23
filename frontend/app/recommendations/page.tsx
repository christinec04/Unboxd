"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import api from "@/app/api/index";
import { NavBar } from "@/components/nav-bar";
import { useRouter } from "next/navigation";

export default function RecommendationsPage() {
  const searchParams = useSearchParams();
  const [username, setUsername] = useState(searchParams.get("username"));
  const [movies, setMovies] = useState([]);

  useEffect(() => {
    async function fetchMovies() {
      const res = await api.get(`/movies/?username=${username}`);
      setMovies(res.data);
      console.log(res.data)
    }
    fetchMovies();
  }, [username]);
  
  // Submit username to backend
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!username) { return; }

    try {
      await api.post('/usernames/', { username: username });
    }
    catch (error) {
      console.error(error);
      return;
    }

    // Navigate to next page
    router.push(`/recommendations?username=${username}`);
  };
  

  return (
    <div className="min-h-screen bg-background">
      <NavBar username={username} setUsername={setUsername} handleSubmit={handleSubmit} />
      
      <h1>Recommendations for {username}</h1>
      <ul>
        {movies.map((m) => (
          <li key={m.title}>{m.title}</li>
        ))}
      </ul>
    </div>
  );
}
