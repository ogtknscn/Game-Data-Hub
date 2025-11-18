import { useState, useEffect } from 'react'
import { TextField, TableCell } from '@mui/material'
import { Column } from '../../types/domain'

interface EditableCellProps {
  value: any
  column: Column
  rowId: number
  onSave: (rowId: number, columnName: string, value: any) => void
}

export default function EditableCell({ value, column, rowId, onSave }: EditableCellProps) {
  const [editing, setEditing] = useState(false)
  const [editValue, setEditValue] = useState(value ?? '')

  useEffect(() => {
    setEditValue(value ?? '')
  }, [value])

  const handleClick = () => {
    setEditing(true)
  }

  const handleBlur = () => {
    setEditing(false)
    if (editValue !== value) {
      onSave(rowId, column.name, editValue)
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleBlur()
    } else if (e.key === 'Escape') {
      setEditValue(value ?? '')
      setEditing(false)
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    let newValue: any = e.target.value

    // Type conversion based on column data type
    if (column.data_type === 'integer') {
      newValue = newValue === '' ? null : parseInt(newValue, 10)
      if (isNaN(newValue as number)) {
        return // Don't update if invalid
      }
    } else if (column.data_type === 'float') {
      newValue = newValue === '' ? null : parseFloat(newValue)
      if (isNaN(newValue as number)) {
        return // Don't update if invalid
      }
    } else if (column.data_type === 'boolean') {
      newValue = e.target.checked
    }

    setEditValue(newValue)
  }

  if (editing) {
    if (column.data_type === 'boolean') {
      return (
        <TableCell>
          <input
            type="checkbox"
            checked={editValue === true || editValue === 'true'}
            onChange={handleChange}
            onBlur={handleBlur}
            autoFocus
          />
        </TableCell>
      )
    }

    return (
      <TableCell padding="none">
        <TextField
          value={editValue}
          onChange={handleChange}
          onBlur={handleBlur}
          onKeyDown={handleKeyDown}
          type={column.data_type === 'integer' || column.data_type === 'float' ? 'number' : 'text'}
          size="small"
          fullWidth
          autoFocus
          variant="standard"
          InputProps={{
            disableUnderline: true,
            sx: { padding: '8px' },
          }}
        />
      </TableCell>
    )
  }

  return (
    <TableCell onClick={handleClick} sx={{ cursor: 'pointer', '&:hover': { backgroundColor: 'action.hover' } }}>
      {value ?? '-'}
    </TableCell>
  )
}

