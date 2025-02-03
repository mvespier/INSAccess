import { useState, useEffect } from "react";

const useWindowDimensions = () => {
  const [dimensions, setDimensions] = useState({
    width: window.innerWidth,
    height: window.innerHeight,
  });

  useEffect(() => {
    const handleResize = () => {
      setDimensions({ width: window.innerWidth, height: window.innerHeight });
    };
    window.addEventListener("resize", handleResize);
    return () => window.removeEventListener("resize", handleResize);
  }, []);

  return dimensions;
};

class DataContainer{
  data = null;

  constructor(data){
    this.data = data
  }

  getData(){
    return this.data
  }
}

export { useWindowDimensions, DataContainer };