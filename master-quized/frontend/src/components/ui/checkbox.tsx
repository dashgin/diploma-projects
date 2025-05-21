import { Checkbox as ChakraCheckbox } from "@chakra-ui/react"
import * as React from "react"

// Use a type to get CheckedChangeDetails type from Chakra
type CheckedChangeDetails = Parameters<
  NonNullable<ChakraCheckbox.RootProps["onCheckedChange"]>
>[0]

export interface CheckboxProps
  extends Omit<ChakraCheckbox.RootProps, "onCheckedChange"> {
  icon?: React.ReactNode
  inputProps?: React.InputHTMLAttributes<HTMLInputElement>
  rootRef?: React.Ref<HTMLLabelElement>
  checked?: boolean
  onCheckedChange?: (details: CheckedChangeDetails) => void
}

export const Checkbox = React.forwardRef<HTMLInputElement, CheckboxProps>(
  function Checkbox(props, ref) {
    const {
      icon,
      children,
      inputProps,
      rootRef,
      checked,
      onCheckedChange,
      ...rest
    } = props

    return (
      <ChakraCheckbox.Root
        ref={rootRef}
        checked={checked}
        onCheckedChange={onCheckedChange}
        {...rest}
      >
        <ChakraCheckbox.HiddenInput ref={ref} {...inputProps} />
        <ChakraCheckbox.Control>
          {icon || <ChakraCheckbox.Indicator />}
        </ChakraCheckbox.Control>
        {children != null && (
          <ChakraCheckbox.Label>{children}</ChakraCheckbox.Label>
        )}
      </ChakraCheckbox.Root>
    )
  },
)
