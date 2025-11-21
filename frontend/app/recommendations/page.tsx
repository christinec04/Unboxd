"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import api from "@/app/api/index";
import { NavBar } from "@/components/nav-bar";

export default function RecommendationsPage() {
  const searchParams = useSearchParams();
  const username = searchParams.get("username");
  const [movies, setMovies] = useState([]);

  useEffect(() => {
    async function fetchMovies() {
      const res = await api.get(`/movies?username=${username}`);
      setMovies(res.data);
    }
    fetchMovies();
  }, [username]);

  return (
    <div>
      <NavBar />
      <h1>Recommendations for {username}</h1>
      <ul>
        {movies.map((m) => (
          <li key={m.title}>{m.title}</li>
        ))}
      </ul>
    </div>
  );
}
