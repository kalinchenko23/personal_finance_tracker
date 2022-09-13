import clsx from 'clsx';
import * as React from 'react';

export default function Accent({
  children,
  className,
  ...rest
}: React.ComponentPropsWithoutRef<'span'>) {
  return (
    <span
      className={clsx(
        'font-bold text-transparent bg-gradient-to-tr from-primary-900 via-primary-600 to-primary-500 bg-clip-text',
        className
      )}
      {...rest}
    >
      {children}
    </span>
  );
}