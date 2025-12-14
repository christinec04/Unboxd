import {
  Empty,
  EmptyContent,
  EmptyDescription,
  EmptyHeader,
  EmptyTitle,
} from "@/components/ui/empty";
import { Button } from "@/components/ui/button";
import { RefreshCcwIcon } from "lucide-react";
import { Status } from "@/app/api/types.gen";
import { Spinner } from "@/components/ui/spinner";

type ExtendedStatus = Status | "ERROR";

export function StatusIndicator({status}: {status: ExtendedStatus}) {
  const isError = status === "ERROR";

  const refreshPage = () => {
    window.location.reload(); 
  };

  return (
    <section className="py-24 relative overflow-hidden flex justify-center">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative">
        <Empty>
          <EmptyHeader>
            <EmptyTitle>
              {status} 
              {!isError && <Spinner className="ml-2 inline-block"/> }
            </EmptyTitle>

            <EmptyDescription>
              {isError && "Something went wrong. Please try searching for another username" }
            </EmptyDescription>
          </EmptyHeader>

          {isError && <EmptyContent>
            <Button variant="outline" size="sm" onClick={refreshPage}>
              <RefreshCcwIcon />
              Refresh
            </Button>
          </EmptyContent>}
        </Empty>
      </div>
    </section>
  )
}
