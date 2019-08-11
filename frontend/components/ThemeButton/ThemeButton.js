import React from 'react';	
import classNames from 'classnames';	
import { Button } from 'reactstrap';	
import classes from './ThemeButton.css';	


 const ThemeButton = React.forwardRef((props, ref) => {	
  const { outline, ...rest } = props;	

   return (	
    <Button className={classNames({	
              [classes.btn]: true,	
              [classes.outline]: outline	
            })}	
            ref={ref}	
            {...rest} />	
  )	
})	

 export default ThemeButton;
 