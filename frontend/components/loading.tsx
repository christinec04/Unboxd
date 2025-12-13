import React from "react";
import { Status } from "@/app/api/types.gen";
import { Progress } from "@/components/ui/progress";

export function Loading({ status }: { status: Status }) {
  const [progress, setProgress] = React.useState(0);

  React.useEffect(() => {
    let timer: NodeJS.Timeout;

    if (status === Status.STARTING) {
      // Increment progress smoothly until ~90%
      timer = setInterval(() => {
        setProgress((prev) => {
          if (prev < 90) return prev + 2; // step size
          return prev;
        });
      }, 200); // every 200ms
    }

    if (status === Status.FINISHED) {
      // Jump to 100% when finished
      setProgress(100);
    }

    if (!status || status === undefined) {
      // Reset when idle or failed
      setProgress(0);
    }

    return () => clearInterval(timer);
  }, [status]);

  // Only render while loading
  if (status !== Status.STARTING) return null;

  return (
    <section className="py-24 relative overflow-hidden flex flex-1 items-end justify-center">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative flex justify-center">
        <Progress value={progress} className="w-[60%]" />
      </div>
    </section>
  );
}