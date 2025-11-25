"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import api from "@/app/api/index";
import { NavBar } from "@/components/nav-bar";
import { useRouter } from "next/navigation";
import { Loading } from "@/components/progress";
import { Result } from "@/components/result";
import { Error } from "@/components/error";

export default function RecommendationsPage() {
  const searchParams = useSearchParams();
  const [username, setUsername] = useState(searchParams.get("username"));
  const [movies, setMovies] = useState([]);
  const router = useRouter();
  const [status, setStatus] = useState('success');

  // On page load, fetch recommended movies
  useEffect(() => {
    async function fetchMovies() {
      const res = await api.get(`/movies/?username=${username}`);
      setMovies(res.data);
      console.log(res.data)
    }

    // Assumes username exists in Letterboxd, and user has review data
    try {
      fetchMovies();
    }
    catch (e) {
      console.error(e);
    }
  
  }, [username]);
  
  // Submit username to backend
  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    if (!username) { return; }

    try {
      setStatus('loading');
      await api.post('/usernames/', { username: username });
      setStatus('success');
    }
    catch (e) {
      setStatus(String(e));
      console.error(e);
      return;
    }

    // Navigate to next page
    router.push(`/recommendations?username=${username}`);
  };
  

  return (
    <div className="min-h-screen w-full bg-background flex flex-col">
      <NavBar username={username} setUsername={setUsername} handleSubmit={handleSubmit} />

      {status === 'loading' && <Loading />} {/* loading doesn't work atm */}
      {status === 'success' && <Result movies={movies} />}
      {status !== 'loading' && status !== 'success' && <Error message={status}/>}
      
    </div>
  );
}
