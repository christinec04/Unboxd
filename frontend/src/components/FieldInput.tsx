import { useState } from "react";
import {
  Field,
  FieldDescription,
  FieldLabel,
} from "@/components/ui/field"
import { Input } from "@/components/ui/input"
import api from '../api';

export function FieldInput() {
  const [username, setUsername] = useState("");

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (username) {
      try {
        await api.post(`/usernames/?username=${username}`);
        setInterval(async () => {
          const response = await api.get(`/status/?username=${username}`);
          console.log(JSON.stringify(response.data));
        }, 500);
      } catch (error) {
        console.error("Error sending username to backend", error);
      }
    }
  };

  return (
    <div className="w-full max-w-md">
      <form onSubmit={handleSubmit}>
        <Field>
          <FieldLabel htmlFor="username">Username</FieldLabel>
          <Input
            id="username"
            type="text"
            placeholder="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
          />
          <FieldDescription>
            Please enter your Letterboxd username
          </FieldDescription>
        </Field>
      </form>
    </div>
  )
}
