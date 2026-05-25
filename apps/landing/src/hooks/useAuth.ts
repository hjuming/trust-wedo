import { useContext } from 'react'
import { AuthContext } from '../contexts/authContextValue'

export const useAuth = () => useContext(AuthContext)
