import { Flex, useBreakpointValue } from "@chakra-ui/react"
import { Link } from "@tanstack/react-router"

import UserMenu from "./UserMenu"

function Navbar() {
  const display = useBreakpointValue({ base: "none", md: "flex" })

  return (
    <Flex
      display={display}
      justify="space-between"
      position="sticky"
      color="white"
      align="center"
      bg="bg.muted"
      w="100%"
      top={0}
      px={4}
      py={2}
    >
      <Link to="/">
        <Flex fontSize="2xl" fontWeight="bold" color="black">
          QuizEd
        </Flex>
      </Link>
      <Flex gap={2} alignItems="center">
        <UserMenu />
      </Flex>
    </Flex>
  )
}

export default Navbar
