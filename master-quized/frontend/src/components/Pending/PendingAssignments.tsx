import { Table } from "@chakra-ui/react"
import { SkeletonText } from "../ui/skeleton"

const PendingAssignments = () => (
  <Table.Root size={{ base: "sm", md: "md" }}>
    <Table.Header>
      <Table.Row>
        <Table.ColumnHeader>ID</Table.ColumnHeader>
        <Table.ColumnHeader>Quiz ID</Table.ColumnHeader>
        <Table.ColumnHeader>Student ID</Table.ColumnHeader>
        <Table.ColumnHeader>Due Date</Table.ColumnHeader>
        <Table.ColumnHeader>Status</Table.ColumnHeader>
      </Table.Row>
    </Table.Header>
    <Table.Body>
      {[...Array(5)].map((_, index) => (
        <Table.Row key={index}>
          <Table.Cell>
            <SkeletonText noOfLines={1} />
          </Table.Cell>
          <Table.Cell>
            <SkeletonText noOfLines={1} />
          </Table.Cell>
          <Table.Cell>
            <SkeletonText noOfLines={1} />
          </Table.Cell>
          <Table.Cell>
            <SkeletonText noOfLines={1} />
          </Table.Cell>
          <Table.Cell>
            <SkeletonText noOfLines={1} />
          </Table.Cell>
        </Table.Row>
      ))}
    </Table.Body>
  </Table.Root>
)

export default PendingAssignments
