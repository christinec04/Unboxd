"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import api from "@/app/api/index";
import { NavBar } from "@/components/nav-bar";
import { useRouter } from "next/navigation";
import { Loading } from "@/components/result/progress";
import { Result } from "@/components/result/result";
import { NotFound } from "@/components/result/not-found";

export default function RecommendationsPage() {
  const searchParams = useSearchParams();
  const [username, setUsername] = useState(searchParams.get("username"));
  const [movies, setMovies] = useState([]);
  const router = useRouter();
  const [status, setStatus] = useState<'loading' | 'notfound' | 'success'>('success');

  // On page load, fetch recommended movies
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
    <div className="min-h-screen bg-background flex flex-col">
      <NavBar username={username} setUsername={setUsername} handleSubmit={handleSubmit} />

      {status === 'loading' && <Loading />}
      {status === 'notfound' && <NotFound />}
      {status === 'success' && <Result />}
      
    </div>
  );
}
