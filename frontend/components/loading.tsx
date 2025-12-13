import {
  Empty,
  EmptyDescription,
  EmptyHeader,
  EmptyTitle,
} from "@/components/ui/empty"
import { Status } from "@/app/api/types.gen";
import { Progress } from "@/components/ui/progress";
import { startTurbopackTraceServer } from "next/dist/build/swc/generated-native";

export function Loading({ status }: { status: Status }) {
  const progress = {
    [Status.STARTING]: 10,
    [Status.VALIDATING_USERNAME]: 20,
    [Status.WAITING_FOR_SCRAPER]: 30,
    [Status.SCRAPING_THE_USER_REVIEWS]: 40,
    [Status.PREPROCESSING_DATA]: 50,
    [Status.FINDING_RECOMMENDATIONS]: 80,
    [Status.FINISHED]: 100
  };

  type LoadingStatus =
  | Status.STARTING
  | Status.VALIDATING_USERNAME
  | Status.WAITING_FOR_SCRAPER
  | Status.SCRAPING_THE_USER_REVIEWS
  | Status.PREPROCESSING_DATA
  | Status.FINDING_RECOMMENDATIONS;


  return (
    <section className="py-24 relative overflow-hidden flex flex-1 items-end justify-center">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative flex justify-center">
        <Empty>
          <EmptyHeader>
            <EmptyTitle>{status}</EmptyTitle>
            <Progress value={progress[status as LoadingStatus]} className="w-[100%]" />
          </EmptyHeader>
        </Empty>
      </div>
    </section>
  );
}