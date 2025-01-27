import { useState } from "react";

import "./App.css";
import SubirArchivo from "./components/SubirArchivo";

function App() {
  const [count, setCount] = useState(0);

  return (
    <>
      
      <SubirArchivo />
    </>
  );
}

export default App;
