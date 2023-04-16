import { createContext, Dispatch, FC, ReactNode, SetStateAction, useContext, useState } from 'react';

type ErrorState = [string, Dispatch<SetStateAction<string>>];

const ErrorContext = createContext<ErrorState>(undefined as never);

type Props = {
  children: ReactNode;
};

export const ErrorProvider: FC<Props> = ({ children }) => {
  const errorState = useState('');

  return <ErrorContext.Provider value={errorState}>{children}</ErrorContext.Provider>;
};

const useError = (): ErrorState => useContext(ErrorContext);

export default useError;
