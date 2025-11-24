"use client"

import * as React from "react"

import { Progress } from "@/components/ui/progress"

export function Loading() {
  const [progress, setProgress] = React.useState(13)

  React.useEffect(() => {
    const timer = setTimeout(() => setProgress(66), 500)
    return () => clearTimeout(timer)
  }, [])

  return (
    <section className="py-24 relative overflow-hidden flex flex-1 items-end justify-center">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative flex justify-center">
        <Progress value={progress} className="w-[60%]" />
      </div>
    </section>
  );
}
