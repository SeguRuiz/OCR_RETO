import { useState } from "react";

import "./App.css";
import SubirArchivo from "./components/SubirArchivo";
import { Card, CardActionArea, CardContent, Stack } from "@mui/material";
import ArhcivosPreview from "./components/ArhcivosPreview";

function App() {
  const [count, setCount] = useState(0);
  const [contenidos, setContenidos] = useState([]);

  return (
    <>
      <Card
        sx={{
          padding: "5px",
          backgroundColor: "#F8FAFD",
        }}
        variant="outlined"
      >
        <CardActionArea>
          <SubirArchivo setContenidos={setContenidos} contenidos={contenidos} />
        </CardActionArea>

        <CardContent sx={{}}>
          <ArhcivosPreview archivos={contenidos} />
        </CardContent>
      </Card>
    </>
  );
}

export default App;
