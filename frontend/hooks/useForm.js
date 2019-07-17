import { useState } from 'react';

const useForm = (initialValues={}) => {
  const [values, setValues] = useState(initialValues);

  const onChange = event => {
    event.persist();
    setValues(values => ({ 
      ...values, 
      [event.target.name]: event.target.value 
    }));
  };

  const reset = () => {
    setValues(initialValues);
  }

  return {
    onChange,
    values,
    reset
  }
};

export default useForm;
