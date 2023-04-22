import { FC, useState } from 'react';
import { Skeleton } from '@mui/material';

type Props = {
  image: string;
  alt: string;
  height: number;
};

const ImageWithSkeleton: FC<Props> = ({ image, alt, height }) => {
  const [showImage, setShowImage] = useState(false);

  return (
    <>
      {!showImage && <Skeleton variant="rectangular" height={height} width={'100%'}/>}
      <img
        alt={alt}
        src={image}
        height={height}
        style={{ display: showImage ? 'block' : 'none', objectFit: 'cover', width: '100%', height: '100%' }}
        onLoad={() => setShowImage(true)}
      />
    </>
  );
};

export default ImageWithSkeleton;
