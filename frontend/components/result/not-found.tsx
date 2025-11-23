import {
  Empty,
  EmptyDescription,
  EmptyHeader,
  EmptyTitle,
} from "@/components/ui/empty"

export function NotFound() {
  return (
    <Empty>
      <EmptyHeader>
        <EmptyTitle>User Not Found</EmptyTitle>
        <EmptyDescription>
          Try searching for another username
        </EmptyDescription>
      </EmptyHeader>
    </Empty>
  )
}
