import {
  Empty,
  EmptyDescription,
  EmptyHeader,
  EmptyTitle,
} from "@/components/ui/empty"

export function Error(status: {message: string}) {
  return (
    <section className="py-24 relative overflow-hidden flex flex-1 items-end justify-center">
      <div className="container mx-auto px-4 sm:px-6 lg:px-8 relative">
        <Empty>
          <EmptyHeader>
            <EmptyTitle>{status.message}</EmptyTitle>
            <EmptyDescription>
              Try searching for another username
            </EmptyDescription>
          </EmptyHeader>
        </Empty>
      </div>
    </section>
  )
}
