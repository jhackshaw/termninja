import React from 'react';
import ThemeButton from '../../../ThemeButton';
import Link from 'next/link';


const AuthLinks = props => {

  return (
    <div className="text-center">
      <Link href="/login" passHref>
        <ThemeButton color="link">
          Login / Register
        </ThemeButton>
      </Link>
    </div>
  )
}

export default AuthLinks;
