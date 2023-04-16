import { createContext, Dispatch, FC, ReactNode, SetStateAction, useContext, useState } from 'react';

type LoadingState = [boolean, Dispatch<SetStateAction<boolean>>];

const LoadingContext = createContext<LoadingState>(undefined as never);

type Props = {
  children: ReactNode;
};

export const LoaderProvider: FC<Props> = ({ children }) => {
  const loading = useState(false);

  return <LoadingContext.Provider value={loading}>{children}</LoadingContext.Provider>;
};

const useLoader = (): LoadingState => useContext(LoadingContext);

export default useLoader;
